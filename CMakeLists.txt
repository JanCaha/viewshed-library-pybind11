cmake_minimum_required(VERSION 3.20)
project(viewshed_pybind)

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

find_package(GDAL REQUIRED)
find_package(SimpleRasters REQUIRED)
find_package(Viewshed REQUIRED)

include_directories(
    SimpleRasters::simplerasters
    Viewshed::viewshed
    cpp_module
    pybind11/include
)

set(SOURCES
    cpp_module/python_module.cpp
    cpp_module/visibility_algorithms.h
    cpp_module/visibility_algorithms.cpp
    cpp_module/python_objects_utils.h
    cpp_module/python_objects_utils.cpp
)

# Find the pybind11 package
include(cmake/QueryPythonForPybind11.cmake)
find_pybind11_python_first()

pybind11_add_module(_viewshed ${SOURCES})

target_compile_definitions(_viewshed PRIVATE
    MODULE_NAME=$<TARGET_FILE_BASE_NAME:_viewshed>
)

target_include_directories(_viewshed PRIVATE ${CMAKE_SOURCE_DIR})

target_link_libraries(_viewshed PRIVATE
    SimpleRasters::SimpleRasters
    Viewshed::viewshed
    GDAL::GDAL
)

# Hide all symbols by default (including external libraries on Linux)
set_target_properties(_viewshed PROPERTIES
    CXX_VISIBILITY_PRESET "hidden"
    VISIBILITY_INLINES_HIDDEN true)

if(CMAKE_SYSTEM_NAME MATCHES "Linux")
    target_link_options(_viewshed PRIVATE "LINKER:--exclude-libs,ALL")
endif()

install(TARGETS _viewshed
    EXCLUDE_FROM_ALL
    COMPONENT python_modules
    DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME})

# Install the debug file for the Python module (Windows only)
if(WIN32)
    install(FILES $<TARGET_PDB_FILE:_add_module>
        EXCLUDE_FROM_ALL
        COMPONENT python_modules
        DESTINATION ${PY_BUILD_CMAKE_MODULE_NAME}
        OPTIONAL)
endif()

option(WITH_PY_STUBS
    "Generate Python stub files (.pyi) for the Python module." On)

if(WITH_PY_STUBS)
    message(STATUS "Generating Python stub files for the Python module.")
    include(cmake/Pybind11Stubgen.cmake)
    pybind11_stubgen(_viewshed)
    pybind11_stubgen_install(_viewshed ${PY_BUILD_CMAKE_MODULE_NAME})
endif()