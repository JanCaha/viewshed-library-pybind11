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
    m.doc() = "Python interface for viewshed library.";

    // library version
    py::object ver = py::cast( ViewshedLibrary::version() );
    m.attr( "version" ) = ver;
    m.attr( "__version__" ) = ver;

    // visibility algorithms
    py::class_<VisibilityAlgs, std::shared_ptr<VisibilityAlgs>>( m, "VisibilityAlgorithms",
                                                                 "Class for storing visibility indices algorithms." )
        .def( py::init( []() { return std::make_shared<VisibilityAlgs>( false ); } ),
              "Build all algorithms. With default NoData value." )
        .def( py::init( []( const double &noData ) { return std::make_shared<VisibilityAlgs>( false, noData ); } ),
              "Build all algorithms with provided NoData value." )
        .def( py::init( []( const bool &single ) { return std::make_shared<VisibilityAlgs>( single ); } ),
              "Build only boolean visibility with default NoData value." )
        .def( py::init( []( const bool &single, const double &noData )
                        { return std::make_shared<VisibilityAlgs>( single, noData ); } ),
              "Build only boolean visibility with provided NoData value." )
        .def( "size", &VisibilityAlgs::size );

    // input raster
    py::class_<ProjectedSquareCellRaster, std::shared_ptr<ProjectedSquareCellRaster>>(
        m, "ProjectedSquareCellRaster", "Class representing raster data." )
        .def( py::init(
                  []( const std::string &path, const int &band )
                  { return std::make_shared<ProjectedSquareCellRaster>( path, GDALDataType::GDT_Unknown, band ); } ),
              "Build from string path and  specified band." )
        .def( py::init( []( const std::string &path ) { return std::make_shared<ProjectedSquareCellRaster>( path ); } ),
              "Build from string path." )
        .def(
            py::init( []( const py::object obj )
                      { return std::make_shared<ProjectedSquareCellRaster>( get_absolute_path( obj, "filename" ) ); } ),
            "Build from pathlib.Path." )
        .def( "error", &ProjectedSquareCellRaster::error, "Error message from the raster." )
        .def( "noData", &ProjectedSquareCellRaster::noData, "NoData value of the raster." );

    // point either viewpoint or target point
    py::class_<Point, std::shared_ptr<Point>>( m, "Point", "Point representing either observer or target point." )
        .def(
            py::init( []( const double &x, const double &y, const std::shared_ptr<ProjectedSquareCellRaster> &dem,
                          const double &offset ) { return std::make_shared<Point>( OGRPoint( x, y ), dem, offset ); } ),
            "Construct using coordinates x,y, ProjectedSquareCellRaster and offset from surface." )
        .def( "isValid", &Point::isValid, "Check that point is valid, with respect to provided DEM model." );

    // viewshed
    py::class_<Viewshed, std::shared_ptr<Viewshed>>( m, "Viewshed", "Class for calculation of visibility from point." )
        .def( py::init( []( const std::shared_ptr<Point> &vp, const std::shared_ptr<ProjectedSquareCellRaster> &dem,
                            std::shared_ptr<VisibilityAlgs> &algs )
                        { return std::make_shared<Viewshed>( vp, dem, algs->get() ); } ),
              "Create class from point, dem and  visibility indices algorithms.." )
        .def(
            "calculate",
            []( const std::shared_ptr<Viewshed> v )
            { v->calculate( []( std::string text, double time ) {}, []( int i, int j ) {} ); },
            "Calculate without callbacks." )
        .def( "calculate", &Viewshed::calculate, "Calculate with specified callbacks." )
        .def(
            "saveResults", []( const std::shared_ptr<Viewshed> v, const std::string path ) { v->saveResults( path ); },
            "Store results at specified path." )
        .def(
            "saveResults",
            []( const std::shared_ptr<Viewshed> v, const py::object path )
            { v->saveResults( get_absolute_path( path, "path" ) ); },
            "Store results at specified pathlib.Path." )
        .def( "setMaxThreads", &Viewshed::setMaxThreads, "Set maximum number of threads to use." )
        .def( "setVisibilityMask", &Viewshed::setVisibilityMask,
              "Specifiy visibility mask to use during calculation." );

    // inverseviewshed
    py::class_<InverseViewshed, std::shared_ptr<InverseViewshed>>( m, "InverseViewshed",
                                                                   "Class for calculation of visibility of point." )
        .def(
            py::init( []( const std::shared_ptr<Point> &tp, const double &offset,
                          const std::shared_ptr<ProjectedSquareCellRaster> &dem, std::shared_ptr<VisibilityAlgs> &algs )
                      { return std::make_shared<InverseViewshed>( tp, offset, dem, algs->get() ); } ),
            "Create class from target point, observer's offset, dem and visibility indices algorithms." )
        .def(
            "calculate",
            []( const std::shared_ptr<InverseViewshed> v )
            { v->calculate( []( std::string text, double time ) {}, []( int i, int j ) {} ); },
            "Calculate without callbacks." )
        .def( "calculate", &InverseViewshed::calculate, "Calculate with specified callbacks." )
        .def(
            "saveResults",
            []( const std::shared_ptr<InverseViewshed> v, const std::string path ) { v->saveResults( path ); },
            "Store results at specified path." )
        .def(
            "saveResults",
            []( const std::shared_ptr<InverseViewshed> v, const py::object path )
            { v->saveResults( get_absolute_path( path, "path" ) ); },
            "Store results at specified pathlib.Path." )
        .def( "setMaxThreads", &InverseViewshed::setMaxThreads, "Set maximum number of threads to use." )
        .def( "setVisibilityMask", &Viewshed::setVisibilityMask,
              "Specifiy visibility mask to use during calculation." );
    ;
}