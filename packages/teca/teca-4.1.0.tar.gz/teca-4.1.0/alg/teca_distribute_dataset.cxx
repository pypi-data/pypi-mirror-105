#include "teca_distribute_dataset.h"

#include "teca_metadata.h"
#include "teca_priority_queue.h"

#include <algorithm>
#include <iostream>
#include <string>
#include <map>

#include <mutex>
#include <condition_variable>

#if defined(TECA_HAS_BOOST)
#include <boost/program_options.hpp>
#endif

//#define TECA_DEBUG

struct teca_distribute_dataset::internals_t
{
    internals_t() : sub_comm(MPI_COMM_NULL),
        sub_comm_rank(0), sub_comm_size(1) 
    {}

    ~internals_t()
    {
#if defined(TECA_HAS_MPI)
        if (sub_comm != MPI_COMM_NULL)
            MPI_Comm_free(sub_comm);
#endif
    }

    MPI_Comm sub_comm;
    int sub_comm_rank;
    int sub_somm_size;
};


// --------------------------------------------------------------------------
teca_distribute_dataset::teca_distribute_dataset() :
   group_size(256), internals(new internals_t)
{
    this->set_number_of_input_connections(1);
    this->set_number_of_output_ports(1);
}

// --------------------------------------------------------------------------
teca_distribute_dataset::~teca_distribute_dataset()
{
    delete this->internals;
}

#if defined(TECA_HAS_BOOST)
// --------------------------------------------------------------------------
void teca_distribute_dataset::get_properties_description(
    const std::string &prefix, options_description &global_opts)
{
    options_description opts("Options for "
        + (prefix.empty()?"teca_distribute_dataset":prefix));

    opts.add_options()

        TECA_POPTS_GET(int, prefix, group_size,
            "Sets the number of MPI ranks in each process group.")

        ;

    this->teca_algorithm::get_properties_description(prefix, opts);

    global_opts.add(opts);
}

// --------------------------------------------------------------------------
void teca_distribute_dataset::set_properties(
    const std::string &prefix, variables_map &opts)
{
    this->teca_algorithm::set_properties(prefix, opts);

    TECA_POPTS_SET(opts, int, prefix, group_size)
}
#endif

// --------------------------------------------------------------------------
teca_metadata teca_distribute_dataset::get_output_metadata(
        unsigned int port,
        const std::vector<teca_metadata> &input_md)
{
    (void)port;

    // partition the communicator into groups of therequested size
#if defined(TECA_HAS_MPI)
    int is_init = 0;
    MPI_Initialized(&is_init);
    if (is_init)
    {
        if (this->internals->sub_comm == MPI_COMM_NULL)
        {
            int rank = 0;
            int n_ranks = 1;

            MPI_Comm comm = this->get_communicator();
            MPI_Comm_rank(comm, &rank);
            MPI_Comm_size(comm, &n_ranks);
        
            MPI_Group world_group = MPI_GROUP_EMPTY;
            MPI_Comm_group(comm, &world_group);
        
            int group_id = rank / this->group_size;
            int group_start = group_id * this->group_size;
            int group_end = std::min(n_ranks, group_start + this->group_size);
            int group_range[3] = {group_start, group_end, 1};
            
            MPI_Group sub_group = MPI_GROUP_EMPTY;
            MPI_Group_incl_range(world_group, 1, range, &sub_group);

            MPI_Comm_create(comm, sub_group, &this->internals->sub_comm);

            MPI_Group_free(&sub_group);
        
            MPI_Comm_rank(this->internals->sub_comm,
                &this->internals->sub_comm_rank);

            MPI_Comm_size(this->internals->sub_comm,
                &this->internals->sub_comm_size);
        }
    }
#endif

    // pass metadata through
    if (input_md.size())
        return teca_metadata(input_md[0]);

    return teca_metadata;
}

// --------------------------------------------------------------------------
std::vector<teca_metadata> teca_distribute_dataset::get_upstream_request(
    unsigned int port,
    const std::vector<teca_metadata> &input_md,
    const teca_metadata &request)
{
#ifdef TECA_DEBUG
    std::cerr << teca_parallel_id()
        << "teca_distribute_dataset::get_upstream_request" << std::endl;
#endif
    (void)port;
    (void)input_md;

    std::vector<teca_metadata> up_reqs;

    // FIXME : only one thread per rank should make the request.

#if defined(TECA_HAS_MPI)
    int is_init = 0;
    MPI_Initialized(&is_init);
    if (is_init)
    {
        if (this->internals->sub_comm == MPI_COMM_NULL)
        {
            TECA_ERROR("Invalid communicator")
            return up_reqs;
        }

        // only rank 0 of the sub communicator makes the request
        if (this->internals->sub_comm_rank == 0)
        {
            std::cerr << teca_parallel_id() << " requesting" << std::endl; 

            // pass the request up
            up_reqs.psuh_back(request);
        }
    }
#endif
    return up_reqs;
}

// --------------------------------------------------------------------------
const_p_teca_dataset teca_distribute_dataset::execute(
    unsigned int port,
    const std::vector<const_p_teca_dataset> &input_data,
    const teca_metadata &request)
{
#ifdef TECA_DEBUG
    std::cerr << teca_parallel_id()
        << "teca_distribute_dataset::execute" << std::endl;
#endif
    (void)port;

    // get the requested index
    std::string request_key;
    if (request.get("index_request_key", request_key))
    {
        TECA_ERROR("Failed to locate the index_request_key")
        return nullptr;
    }

    index_t index = 0;
    if (request.get(request_key, index))
    {
        TECA_ERROR("Failed to get the requested index using the"
            " index_request_key \"" << request_key << "\"")
        return nullptr;
    }

    const_p_teca_dataset data_out;

    // get the cache element associated with the requested index
    p_cache_entry elem;
    {
    std::lock_guard<std::mutex> lock(this->internals->m_mutex);;
    data_map_t::iterator it = this->internals->m_data.find(index);
    if (it == this->internals->m_data.end())
    {
        TECA_ERROR("The cache is in an invalid state")
        return nullptr;
    }
    elem = it->second;
    }

    if (input_data.size())
    {
        // add new data to the cache
        {
        std::lock_guard<std::mutex> elock(elem->m_mutex);
        elem->m_data = input_data[0];
        --elem->m_keep;
        }
        // notify other threads that may be waiting for this data
        elem->m_cond.notify_all();
#ifdef TECA_DEBUG
        std::cerr << teca_parallel_id() << "add data " << index
            << " keep=" << elem->m_keep << std::endl;
#endif
    }
    else
    {
        // fetch existing data from the cache
        if (!elem->m_data)
        {
            // data is not yet ready, it will be provided by another thread
            std::unique_lock<std::mutex> elock(elem->m_mutex);
            if (!elem->m_data)
            {
                // data is not ready wait for another thread to provide
                elem->m_cond.wait(elock, [&]{ return bool(elem->m_data); });
                --elem->m_keep;
            }
        }
        else
        {
            // data is ready
            std::lock_guard<std::mutex> elock(elem->m_mutex);
            --elem->m_keep;
        }
#ifdef TECA_DEBUG
        std::cerr << teca_parallel_id() << "use data " << index
            << " keep=" << elem->m_keep << std::endl;
#endif
    }

    // return the dataset
    data_out = elem->m_data;

    // enforce the max cache size
    {
    std::lock_guard<std::mutex> lock(this->internals->m_mutex);
    unsigned long n_cached = this->internals->m_time_used.size();
    if (n_cached > this->max_cache_size)
    {
#ifdef TECA_DEBUG
        std::cerr << "cache too large " <<  n_cached << std::endl;
        this->internals->m_heap->to_stream(std::cerr, false);
#endif
        // might have to save some elements if they haven't been served yet
        std::vector<index_t> save;
        save.reserve(n_cached);

        unsigned long n_to_rm = n_cached - this->max_cache_size;

        // make one pass over the cache in lru order, or stop if we find
        // enough elements that can be deleted
        for (unsigned long i = 0; n_to_rm && (i < n_cached); ++i)
        {
            index_t idx = this->internals->m_heap->pop();

            p_cache_entry elem = this->internals->m_data[idx];

            // have all requests for the data been served?
            unsigned long keep = 0;
            {
            std::lock_guard<std::mutex> elock(elem->m_mutex);
            keep = elem->m_keep;
            }
            if (keep)
            {
                // no, delete later
                save.push_back(idx);
#ifdef TECA_DEBUG
                std::cerr << teca_parallel_id() << "save "
                    << idx << " keep=" << keep << std::endl;
#endif
            }
            else
            {
                // yes, delete now
                this->internals->m_data.erase(idx);
                this->internals->m_time_used.erase(idx);
                --n_to_rm;
#ifdef TECA_DEBUG
                std::cerr << teca_parallel_id() << "evict "
                    << idx << std::endl;
#endif
            }
        }

        // put elements we couldn't remove because they haven't been
        // served yet back on the heap
        unsigned long n = save.size();
        for (unsigned long i = 0; i < n; ++i)
        {
            this->internals->m_heap->push(save[i]);
        }
    }
    }

    return data_out;
}
