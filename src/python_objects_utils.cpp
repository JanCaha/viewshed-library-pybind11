#include "python_objects_utils.h"

std::string get_absolute_path( py::object obj, std::string variable_name )
{
    py::object Path = py::module_::import( "pathlib" ).attr( "PurePath" );
    if ( !py::isinstance( obj, Path ) )
    {
        throw std::runtime_error( "Error: " + variable_name + " must be PurePath (pathlib)." );
    }

    std::string path = py::str( obj.attr( "as_posix" )() );

    return path;
}