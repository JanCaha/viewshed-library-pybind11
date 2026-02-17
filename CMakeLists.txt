cmake_minimum_required(VERSION 3.24)
project(viewshed_pybind VERSION 0.8.0)

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

find_package(GDAL REQUIRED)
find_package(SimpleRasters REQUIRED)
find_package(Viewshed REQUIRED)

include_directories(
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

target_include_directories(_viewshed PRIVATE ${CMAKE_SOURCE_DIR})

target_link_libraries(_viewshed PRIVATE
    SimpleRasters::simplerasters_shared
    Viewshed::viewshed_shared
    GDAL::GDAL
)

install(TARGETS _viewshed LIBRARY DESTINATION viewshed)

option(WITH_PY_STUBS
    "Generate Python stub files (.pyi) for the Python module." OFF)

if(WITH_PY_STUBS)
    message(STATUS "Generating Python stub files for the Python module and formatting them with black.")

    set(PYTHON_PACKAGE_SOURCE_DIR ${CMAKE_SOURCE_DIR}"/src/viewshed")
    set(PYTHON_STUB_FILENAME "_viewshed.pyi")
    set(PYTHON_STUB_PATH ${PYTHON_PACKAGE_SOURCE_DIR}"/"${PYTHON_STUB_FILENAME})
    set(PYTHON_STUB_TEMP_DIR ${CMAKE_BINARY_DIR}"/stubgen")
    set(PYTHON_STUB_TEMP_PACKAGE_DIR ${PYTHON_STUB_TEMP_DIR}"/viewshed")
    set(PYTHON_STUB_TEMP_PATH ${PYTHON_STUB_TEMP_PACKAGE_DIR}"/"${PYTHON_STUB_FILENAME})
    set(PYTHON_STUB_MERGE_SCRIPT ${CMAKE_SOURCE_DIR}"/scripts/merge_stub_fixes.py")

    add_custom_command(
        TARGET _viewshed
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${PYTHON_STUB_TEMP_DIR}
        COMMAND ${Python3_EXECUTABLE} "-m" "pybind11_stubgen" _viewshed "--output" ${PYTHON_STUB_TEMP_DIR}
        COMMAND ${Python3_EXECUTABLE} ${PYTHON_STUB_MERGE_SCRIPT} "--generated" ${PYTHON_STUB_TEMP_PATH} "--existing" ${PYTHON_STUB_PATH} "--output" ${PYTHON_STUB_PATH}
        COMMAND black ${PYTHON_PACKAGE_SOURCE_DIR} "--line-length" "120"
        COMMENT "Copying shared library to python package directory"
    )
endif()