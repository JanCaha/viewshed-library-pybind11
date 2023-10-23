#!bin/bash

set -u
set -e

PWD=`pwd`

FOLDER=pybind_viewshed
PACKAGE=python3-viewshed
VERSION=$(grep "version = " setup.cfg| grep -E -o -e "[0-9\.]+" )

rm -rf build dist .mypy_cache
cd ..
tar -acf "$PACKAGE"_"$VERSION".orig.tar.gz $FOLDER
cd $FOLDER
debuild -S -sa
cd ..
dput ppa:jancaha/gis-tools "$PACKAGE"_"$VERSION"-0ppa0_source.changes