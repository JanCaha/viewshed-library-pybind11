#!bin/bash

set -u
set -e

PWD=`pwd`

FOLDER=pybind_viewshed
PACKAGE=python3-viewshed
DEBIAN_VERSION=$(grep "python3-viewshed (" debian/changelog -m 1 |  grep -E -o -e "[0-9]+\.[0-9]+\.[0-9]+")

rm -rf build dist .mypy_cache .venv
cd ..
tar -acf "$PACKAGE"_"$DEBIAN_VERSION".orig.tar.gz $FOLDER
cd $FOLDER
debuild -S -sa
cd ..
dput ppa:jancaha/gis-tools "$PACKAGE"_"$DEBIAN_VERSION"-0ppa0_source.changes