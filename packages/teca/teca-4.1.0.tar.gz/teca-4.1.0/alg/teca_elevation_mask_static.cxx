#include "teca_elevation_mask.h"

#include "teca_cartesian_mesh.h"
#include "teca_array_collection.h"
#include "teca_variant_array.h"
#include "teca_metadata.h"
#include "teca_array_attributes.h"

#include "teca_dataset_source.h"
#include "teca_dataset_capture.h"
#include "teca_cartesian_mesh_regrid.h"
#include "teca_index_executive.h"

#include <algorithm>
#include <iostream>
#include <string>
#include <set>
#include <cmath>

#if defined(TECA_HAS_BOOST)
#include <boost/program_options.hpp>
#endif

//#define TECA_DEBUG

struct teca_elevation_mask::internals_t
{
    internals_t() {}

    teca_algorithm_output_port surface_elevation_port;  // pipeline that serves up surface elvation field
    const_p_teca_cartesian_mesh surface_elevation;      // 2d surface elevation field

    // compute the valid value mask such that for each point the mask
    // is 1 where the mesh point is above the surface of the Earth and
    // 0 otherwise
    template<typename mask_t, typename elev_num_t, typename mesh_num_t>
    static void mask_by_surface_elevation(
        size_t nx, size_t ny, size_t nz,
        mask_t * __restrict__ mask,
        const elev_num_t * __restrict__ surface_elev,
        const mesh_num_t * __restrict__ mesh_elevation)
    {
        size_t nxy = nx*ny;
        for (size_t k = 0; k < nz; ++k)
        {
            const mesh_num_t * __restrict__ mesh_elev = mesh_elevation + k*nxy;
            for (size_t q = 0; q < nxy; ++q)
            {
                mask[q] = mesh_elev[q] >= (mesh_num_t)surface_elev[q] ? mask_t(1) : mask_t(0);
            }
        }
    }
};


// --------------------------------------------------------------------------
teca_elevation_mask::teca_elevation_mask() :
     mesh_height_variable("zg"), surface_elevation_variable("z"),
    group_size(1024), internals(new internals_t)
{
    this->set_number_of_input_connections(1);
    this->set_number_of_output_ports(1);
}

// --------------------------------------------------------------------------
teca_elevation_mask::~teca_elevation_mask()
{
    delete this->internals;
}

#if defined(TECA_HAS_BOOST)
// --------------------------------------------------------------------------
void teca_elevation_mask::get_properties_description(
    const std::string &prefix, options_description &global_opts)
{
    options_description opts("Options for "
        + (prefix.empty()?"teca_elevation_mask":prefix));

    opts.add_options()

        TECA_POPTS_GET(std::string, prefix, surface_elevation_variable,
            "Set the name of the variable containing surface elevation"
            " values in meters above mean sea level")

        TECA_POPTS_GET(std::string, prefix, mesh_height_variable,
            "Set the name of the variable containing point wise mesh height"
            " values in meters above mean sea level")

        TECA_POPTS_MULTI_GET(std::vector<std::string>, prefix, mask_variables,
            "Set the names of the variables to store the generated mask in."
            " Each name is assigned a reference to the mask.")

        TECA_POPTS_GET(int, prefix, group_size,
            "Sets the number of MPI ranks in each process group that reads"
            " surface elevation")
        ;

    this->teca_algorithm::get_properties_description(prefix, opts);

    global_opts.add(opts);
}

// --------------------------------------------------------------------------
void teca_elevation_mask::set_properties(
    const std::string &prefix, variables_map &opts)
{
    this->teca_algorithm::set_properties(prefix, opts);

    TECA_POPTS_SET(opts, std::string, prefix, surface_elevation_variable)
    TECA_POPTS_SET(opts, std::string, prefix, mesh_height_variable)
    TECA_POPTS_SET(opts, std::vector<std::string>, prefix, mask_variables)
    TECA_POPTS_SET(opts, int, prefix, group_size)
}
#endif

// --------------------------------------------------------------------------
void teca_elevation_mask::set_input_connection(unsigned int id,
        const teca_algorithm_output_port &port)
{
    if (id == 1)
        this->internals->surface_elevation_port = port;
    else
        this->teca_algorithm::set_input_connection(0, port);
}


// --------------------------------------------------------------------------
teca_metadata teca_elevation_mask::get_output_metadata(
    unsigned int port,
    const std::vector<teca_metadata> &input_md)
{
#ifdef TECA_DEBUG
    cerr << teca_parallel_id()
        << "teca_elevation_mask::get_output_metadata" << endl;
#endif
    (void)port;

    // because of thread safety, and MPI communication, this can only run once
    // the first time through
    if (!internals->surface_elevation)
    {
        int rank = 0;
#if defined(TECA_HAS_MPI)
        MPI_Comm comm = this->get_communicator();

        int is_init = 0;
        MPI_Initialized(&is_init);
        if (is_init)
        {
            // partition the communicator into groups of the requested size
            /*teca_mpi_util::split_communicator(this->get_communicator(),
                this->group_size, &comm);*/

            MPI_Comm_rank(comm, &rank);
        }
#endif
        // rank 0 loads and distributes the data
        int regrid_stat = 0;
        if (rank == 0)
        {
            // get the input surface elevation metadata
            teca_metadata src_elev_md =
                get_algorithm(this->internals->surface_elevation_port)->update_metadata();

            // get the vertical coordinate from the input surface elevation
            teca_metadata src_elev_coords;
            const_p_teca_variant_array src_elev_z;
            if (src_elev_md.get("coordinates", src_elev_coords) ||
                !(src_elev_z = src_elev_coords.get("z")))
            {
                TECA_ERROR("Failed to get input surface elevation vertical coordinate")
#if defined(TECA_HAS_MPI)
                regrid_stat = -1;
                if (is_init)
                    MPI_Bcast(&regrid_stat, 1, MPI_INT, 0, comm);
#endif
                return teca_metadata();
            }

            // get the horizontal coordinates from the input mesh to mask
            const teca_metadata &in_mesh_md = input_md[0];

            teca_metadata in_mesh_coords;
            in_mesh_md.get("coordinates", in_mesh_coords);

            p_teca_variant_array tgt_elev_x = in_mesh_coords.get("x");
            p_teca_variant_array tgt_elev_y = in_mesh_coords.get("y");
            p_teca_variant_array tgt_elev_z = src_elev_z->new_copy(0, 0);

            // construct the target mesh and its metadata
            unsigned long tgt_elev_x1 = tgt_elev_x->size() - 1;
            unsigned long tgt_elev_y1 = tgt_elev_y->size() - 1;

            unsigned long tgt_elev_whole_extent[6] =
                {0, tgt_elev_x1, 0, tgt_elev_y1, 0, 0};

            double tgt_elev_bounds[6];
            tgt_elev_x->get(0, tgt_elev_bounds[0]);
            tgt_elev_x->get(tgt_elev_x1, tgt_elev_bounds[1]);
            tgt_elev_y->get(0, tgt_elev_bounds[2]);
            tgt_elev_y->get(tgt_elev_y1, tgt_elev_bounds[3]);
            tgt_elev_z->get(0, tgt_elev_bounds[4]);
            tgt_elev_z->get(0, tgt_elev_bounds[5]);

            teca_metadata tgt_elev_coords;
            tgt_elev_coords.set("x", tgt_elev_x);
            tgt_elev_coords.set("y", tgt_elev_y);
            tgt_elev_coords.set("z", tgt_elev_z);

            teca_metadata tgt_elev_md;
            tgt_elev_md.set("coordinates", tgt_elev_coords);
            tgt_elev_md.set("whole_extent", tgt_elev_whole_extent, 6);
            tgt_elev_md.set("bounds", tgt_elev_bounds, 6);
            tgt_elev_md.set("index_initializer_key", std::string("num_steps"));
            tgt_elev_md.set("num_steps", 1);
            tgt_elev_md.set("index_request_key", std::string("step_num"));

            // construct the target surface elevation mesh
            p_teca_cartesian_mesh tgt_elev = teca_cartesian_mesh::New();
            tgt_elev->set_x_coordinates("x", tgt_elev_x);
            tgt_elev->set_y_coordinates("y", tgt_elev_y);
            tgt_elev->set_z_coordinates("z", tgt_elev_z);
            tgt_elev->set_extent(tgt_elev_whole_extent);
            tgt_elev->set_whole_extent(tgt_elev_whole_extent);
            tgt_elev->set_bounds(tgt_elev_bounds);

            // construct the regriding pipeline
            p_teca_dataset_source tgt_elev_source = teca_dataset_source::New();
            tgt_elev_source->set_metadata(tgt_elev_md);
            tgt_elev_source->set_dataset(tgt_elev);

            p_teca_cartesian_mesh_regrid reg = teca_cartesian_mesh_regrid::New();
            reg->set_input_connection(0, tgt_elev_source->get_output_port());
            reg->set_input_connection(1, this->internals->surface_elevation_port);

            p_teca_index_executive exec = teca_index_executive::New();
            exec->set_start_index(0);
            exec->set_end_index(0);
            exec->set_arrays({this->surface_elevation_variable});
            exec->set_bounds(tgt_elev_bounds);

            p_teca_dataset_capture cap = teca_dataset_capture::New();
            cap->set_input_connection(reg->get_output_port());
            cap->set_executive(exec);

            // run the regridding pipeline
            cap->update();

            const_p_teca_cartesian_mesh tgt_elev_out =
                std::dynamic_pointer_cast<const teca_cartesian_mesh>(cap->get_dataset());

            if (!tgt_elev_out)
            {
                TECA_ERROR("Failed to regrid the surface elevation mesh")
#if defined(TECA_HAS_MPI)
                regrid_stat = -1;
                if (is_init)
                    MPI_Bcast(&regrid_stat, 1, MPI_INT, 0, comm);
#endif
                return teca_metadata();
            }

#if defined(TECA_HAS_MPI)
            // signal success
            if (is_init)
                MPI_Bcast(&regrid_stat, 1, MPI_INT, 0, comm);

            // serialize the regridded surface elevations
            teca_binary_stream bs;
            tgt_elev_out->to_stream(bs);

            // share
            bs.broadcast(comm);
#endif
            // cache
            this->internals->surface_elevation = tgt_elev_out;
        }
#if defined(TECA_HAS_MPI)
        else if (is_init)
        {
            // check for regriding error
            MPI_Bcast(&regrid_stat, 1, MPI_INT, 0, comm);
            if (regrid_stat)
            {
                return teca_metadata();
            }

            // receive
            teca_binary_stream bs;
            bs.broadcast(comm);

            p_teca_cartesian_mesh tgt_elev = teca_cartesian_mesh::New();
            if (tgt_elev->from_stream(bs))
            {
                TECA_ERROR("Failed to deserialize the regridded surface elevation")
                return teca_metadata();
            }

            // cache
            this->internals->surface_elevation = tgt_elev;
        }
#endif
    }

    // validate runtime provided settings
    unsigned int n_mask_vars = this->mask_variables.size();
    if (n_mask_vars == 0)
    {
        TECA_ERROR("The names of the output (mask_variables) were not provided")
        return teca_metadata();
    }

    // add the mask arrays we will generate
    teca_metadata out_md(input_md[0]);

    for (unsigned int i = 0; i < n_mask_vars; ++i)
        out_md.append("variables", this->mask_variables[i]);

    // insert attributes to enable this to be written by the CF writer
    teca_metadata attributes;
    out_md.get("attributes", attributes);

    teca_metadata mesh_height_atts;
    if (attributes.get(this->mesh_height_variable, mesh_height_atts))
    {
        TECA_WARNING("Failed to get mesh_height_variable \""
            << this->mesh_height_variable << "\" attrbibutes."
            " Writing the result will not be possible")
    }
    else
    {
        // get the centering and size from the array
        unsigned int centering = 0;
        mesh_height_atts.get("centering", centering);

        unsigned long size = 0;
        mesh_height_atts.get("size", size);

        // construct output attributes
        teca_array_attributes mask_atts(
            teca_variant_array_code<char>::get(),
            centering, size, "none", "", "elevation mask");

        // add one for each output
        for (unsigned int i = 0; i < n_mask_vars; ++i)
            attributes.set(this->mask_variables[i], (teca_metadata)mask_atts);

        // update the attributes collection
        out_md.set("attributes", attributes);
    }

    return out_md;
}

// --------------------------------------------------------------------------
std::vector<teca_metadata> teca_elevation_mask::get_upstream_request(
    unsigned int port,
    const std::vector<teca_metadata> &input_md,
    const teca_metadata &request)
{
    (void)port;
    (void)input_md;

    std::vector<teca_metadata> up_reqs;

    // get the names of the arrays we need to request
    if (this->mesh_height_variable.empty())
    {
        TECA_ERROR("The mesh_height_variable was not specified")
        return up_reqs;
    }

    // input port 0 will source the mesh height field, and any other data
    // requested by the down stream.  copy the incoming request to preserve the
    // downstream requirements and add the mesh height variable
    teca_metadata req_0(request);

    std::set<std::string> arrays;
    if (req_0.has("arrays"))
        req_0.get("arrays", arrays);

    arrays.insert(this->mesh_height_variable);

    // intercept request for our output
    int n_mask_vars = this->mask_variables.size();
    for (int i = 0; i < n_mask_vars; ++i)
        arrays.erase(this->mask_variables[i]);

    req_0.set("arrays", arrays);
    up_reqs.push_back(req_0);

    return up_reqs;
}

// --------------------------------------------------------------------------
const_p_teca_dataset teca_elevation_mask::execute(
    unsigned int port,
    const std::vector<const_p_teca_dataset> &input_data,
    const teca_metadata &request)
{
#ifdef TECA_DEBUG
    cerr << teca_parallel_id() << "teca_elevation_mask::execute" << endl;
#endif
    (void)port;
    (void)request;

    // check that we have the surface elevation
    if (!this->internals->surface_elevation)
    {
        TECA_ERROR("Surface elevation data not available")
        return nullptr;
    }

    // check for an error upstream
    if ((input_data.size() != 1) || !input_data[0])
    {
        TECA_ERROR("Invalid inputs detected")
        return nullptr;
    }

    // get the input 3D mesh
    const_p_teca_cartesian_mesh in_mesh
        = std::dynamic_pointer_cast<const teca_cartesian_mesh>(input_data[0]);

    if (!in_mesh)
    {
        TECA_ERROR("Data to mask on input port 0 is not a"
            " teca_cartesian_mesh. Got " << input_data[0]->get_class_name())
        return nullptr;
    }

    // get the mesh dimensions
    unsigned long extent[6];
    in_mesh->get_extent(extent);

    unsigned long nx = extent[1] - extent[0] + 1;
    unsigned long ny = extent[3] - extent[2] + 1;
    unsigned long nz = extent[5] - extent[4] + 1;

    // get the mesh height, this is a 3d field with the altitude for
    // each mesh point
    const_p_teca_variant_array mesh_height =
        in_mesh->get_point_arrays()->get(this->mesh_height_variable);

    if (!mesh_height)
    {
        TECA_ERROR("Mesh to mask is missing the height field \""
            << this->mesh_height_variable << "\"")
        return nullptr;
    }

    // get the surface elevation, this is a 2d field with surface altitude
    // at each mesh point. regridding has been performed so that the horizontal
    // coordinates are the same as the 3d mesh for which masks will be generated
    const_p_teca_variant_array surface_elev =
        this->internals->surface_elevation->get_point_arrays()->get(this->surface_elevation_variable);

    if (!surface_elev)
    {
        TECA_ERROR("Surface elevation data has no array \""
            << this->surface_elevation_variable << "\"")
        return nullptr;
    }


    // compute the mask
    p_teca_char_array mask = teca_char_array::New(mesh_height->size());
    char *p_mask = mask->get();

    NESTED_TEMPLATE_DISPATCH(const teca_variant_array_impl,
        surface_elev.get(),
        _SURF,

        const NT_SURF *p_surface_elev =
            static_cast<const TT_SURF *>(surface_elev.get())->get();

        NESTED_TEMPLATE_DISPATCH(const teca_variant_array_impl,
            mesh_height.get(),
            _MESH,

            const NT_MESH *p_mesh_height =
                static_cast<const TT_MESH *>(mesh_height.get())->get();


            internals_t::mask_by_surface_elevation(nx, ny, nz,
                p_mask, p_surface_elev, p_mesh_height);

            )

        )

    // allocate the output mesh
    p_teca_cartesian_mesh out_mesh = std::dynamic_pointer_cast<teca_cartesian_mesh>
        (std::const_pointer_cast<teca_cartesian_mesh>(in_mesh)->new_shallow_copy());

    // store the results under the requested names
    int n_mask_vars = this->mask_variables.size();
    for (int i = 0; i < n_mask_vars; ++i)
    {
       out_mesh->get_point_arrays()->set(this->mask_variables[i], mask);
    }

    return out_mesh;
}
