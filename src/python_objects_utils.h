#include <string>

#include <pybind11/pybind11.h>
namespace py = pybind11;

std::string get_absolute_path( py::object obj, std::string variable_name );