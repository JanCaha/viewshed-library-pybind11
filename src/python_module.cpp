#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
namespace py = pybind11;

#include <abstractviewshedalgorithm.h>
#include <inverseviewshed.h>
#include <point.h>
#include <viewshed.h>
#include <viewshedlibrary.h>

#include "simplerasters.h"

#include "python_objects_utils.h"
#include "visibility_algorithms.h"

using viewshed::AbstractViewshedAlgorithm;
using viewshed::InverseViewshed;
using viewshed::Point;
using viewshed::Viewshed;

PYBIND11_MODULE( viewshed, m )
{
    // library version
    py::object ver = py::cast( ViewshedLibrary::version() );
    m.attr( "version" ) = ver;
    m.attr( "__version__" ) = ver;

    // visibility algorithms
    py::class_<VisibilityAlgs, std::shared_ptr<VisibilityAlgs>>( m, "VisibilityAlgorithms" )
        .def( py::init( []() { return std::make_shared<VisibilityAlgs>( false ); } ) )
        .def( py::init( []( const double &noData ) { return std::make_shared<VisibilityAlgs>( false, noData ); } ) )
        .def( py::init( []( const bool &single ) { return std::make_shared<VisibilityAlgs>( single ); } ) )
        .def( py::init( []( const bool &single, const double &noData )
                        { return std::make_shared<VisibilityAlgs>( single, noData ); } ) )
        .def( "size", &VisibilityAlgs::size );

    // input raster
    py::class_<ProjectedSquareCellRaster, std::shared_ptr<ProjectedSquareCellRaster>>( m, "ProjectedSquareCellRaster" )
        .def( py::init(
            []( const std::string &path, const int &band )
            { return std::make_shared<ProjectedSquareCellRaster>( path, GDALDataType::GDT_Unknown, band ); } ) )
        .def(
            py::init( []( const std::string &path ) { return std::make_shared<ProjectedSquareCellRaster>( path ); } ) )
        .def( py::init(
            []( const py::object obj )
            { return std::make_shared<ProjectedSquareCellRaster>( get_absolute_path( obj, "filename" ) ); } ) )
        .def( "error", &ProjectedSquareCellRaster::error )
        .def( "noData", &ProjectedSquareCellRaster::noData );

    // point either viewpoint or target point
    py::class_<Point, std::shared_ptr<Point>>( m, "Point" )
        .def( py::init( []( const double &x, const double &y, const std::shared_ptr<ProjectedSquareCellRaster> &dem,
                            const double &offset )
                        { return std::make_shared<Point>( OGRPoint( x, y ), dem, offset ); } ) )
        .def( "isValid", &Point::isValid );

    // viewshed
    py::class_<Viewshed, std::shared_ptr<Viewshed>>( m, "Viewshed" )
        .def( py::init( []( const std::shared_ptr<Point> &vp, const std::shared_ptr<ProjectedSquareCellRaster> &dem,
                            std::shared_ptr<VisibilityAlgs> &algs )
                        { return std::make_shared<Viewshed>( vp, dem, algs->get() ); } ) )
        .def( "calculate", []( const std::shared_ptr<Viewshed> v )
              { v->calculate( []( std::string text, double time ) {}, []( int i, int j ) {} ); } )
        .def( "calculate", &Viewshed::calculate )
        .def( "saveResults",
              []( const std::shared_ptr<Viewshed> v, const std::string path ) { v->saveResults( path ); } )
        .def( "saveResults", []( const std::shared_ptr<Viewshed> v, const py::object path )
              { v->saveResults( get_absolute_path( path, "path" ) ); } )
        .def( "setMaxThreads", &Viewshed::setMaxThreads )
        .def( "setVisibilityMask", &Viewshed::setVisibilityMask );

    // inverseviewshed
    py::class_<InverseViewshed, std::shared_ptr<InverseViewshed>>( m, "InverseViewshed" )
        .def(
            py::init( []( const std::shared_ptr<Point> &tp, const double &offset,
                          const std::shared_ptr<ProjectedSquareCellRaster> &dem, std::shared_ptr<VisibilityAlgs> &algs )
                      { return std::make_shared<InverseViewshed>( tp, offset, dem, algs->get() ); } ) )
        .def( "calculate", []( const std::shared_ptr<InverseViewshed> v )
              { v->calculate( []( std::string text, double time ) {}, []( int i, int j ) {} ); } )
        .def( "calculate", &InverseViewshed::calculate )
        .def( "saveResults",
              []( const std::shared_ptr<InverseViewshed> v, const std::string path ) { v->saveResults( path ); } )
        .def( "saveResults", []( const std::shared_ptr<InverseViewshed> v, const py::object path )
              { v->saveResults( get_absolute_path( path, "path" ) ); } )
        .def( "setMaxThreads", &InverseViewshed::setMaxThreads )
        .def( "setVisibilityMask", &Viewshed::setVisibilityMask );
    ;
}