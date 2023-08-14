cmake_minimum_required(VERSION 3.20)
project(viewshed_pybind)

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(GDAL REQUIRED)
find_package(SimpleRasters REQUIRED)
find_package(Viewshed REQUIRED)

include_directories(
    impleRasters::simplerasters
    Viewshed::viewshed
    src
    pybind11/incude
)

set(SOURCES
    src/python_module.cpp
    src/visibility_algorithms.h
    src/visibility_algorithms.cpp
    src/python_objects_utils.h
    src/python_objects_utils.cpp
)

add_subdirectory(pybind11)
pybind11_add_module(viewshed ${SOURCES})

target_compile_definitions(viewshed
    PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

target_link_libraries(viewshed PRIVATE 
    SimpleRasters::simplerasters
    Viewshed::viewshed
    GDAL::GDAL
)