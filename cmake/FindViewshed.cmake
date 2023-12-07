include(LibFindMacros)

# Use pkg-config to get hints about paths
libfind_pkg_check_modules(viewshed_PKGCONF viewshed)

# Include dir
find_path(viewshed_INCLUDE_DIR
    NAMES viewshedlibrary.h
    PATHS
    /usr/include
    /usr/include/viewshed
    /usr/local/include/viewshed
    "${CMAKE_PREFIX_PATH}/include"
    ${viewshed_PKGCONF_INCLUDE_DIRS}
)

# Finally the library itself
find_library(viewshed_LIBRARY
    NAMES viewshed
    PATHS
    /usr/lib
    /usr/lib64
    /usr/local/lib
    "${CMAKE_PREFIX_PATH}/lib"
    ${viewshed_PKGCONF_LIBRARY_DIRS}
)

if(viewshed_LIBRARY)
    message(STATUS "Viewshed installed. Found at: ${viewshed_LIBRARY}.")

    if(NOT TARGET Viewshed::viewshed)
        add_library(Viewshed::viewshed UNKNOWN IMPORTED)
        set_target_properties(Viewshed::viewshed PROPERTIES
            IMPORTED_LOCATION "${viewshed_LIBRARY}"
            INTERFACE_INCLUDE_DIRECTORIES "${viewshed_INCLUDE_DIR}")
    endif()
endif()
