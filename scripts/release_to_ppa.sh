#!bin/bash
# DEBEMAIL=jan.caha@outlook.com 
# DEBFULLNAME="Jan Caha"

set -u
set -e

# dch -i "CHANGELOG TEXT"
# dch -r

PWD=`pwd`

FOLDER=pybind_viewshed
PACKAGE=python3-viewshed
MAIN_VERSION=$(grep "python3-viewshed (" debian/changelog -m 1 |  grep -E -o -e "[0-9]+\.[0-9]+\.[0-9]+")
DEBIAN_VERSION=$(grep "python3-viewshed (" debian/changelog -m 1 |  grep -E -o -e "[0-9]+\.[0-9]+\.[0-9]+(-[0-9]+)?")

rm -rf build dist .mypy_cache .venv
cd ..
# tar --exclude='.git' --exclude='tests' --exclude='scripts' --exclude=".github" --exclude=".vscode" --exclude="docker" -acf "$PACKAGE"_"$MAIN_VERSION".orig.tar.gz $FOLDER
cd $FOLDER
debuild -S -sa
cd ..
dput ppa:jancaha/gis-tools "$PACKAGE"_"$DEBIAN_VERSION"_source.changes --passive
# rm $PACKAGE*