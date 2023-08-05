#include <iostream>
#include <type_traits>

template <typename num_t, int len>
std::ostream &to_stream(std::ostream &os, const num_t (& data)[len])
{
    for (int i = 0; i < len; ++i)
        os << ", " << data[i];
    return os;
}


template <typename num_t, int len, typename = typename std::enable_if<!std::is_same<num_t,char>::value,bool>::type>
std::ostream &operator<<(std::ostream &os, const num_t (& data)[len])
{
    std::cerr << "called" << std::endl;
    return to_stream(os, data);
}

int main(int, char**)
{
    double dat[6] = {0,1,2,3,4,5};

    std::cerr << "data=" << dat << std::endl;

    //to_stream(std::cerr, dat);
    //std::cerr << std::endl;

    return 0;
}






