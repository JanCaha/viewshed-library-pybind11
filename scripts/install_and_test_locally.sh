#!/bin/bash
VENV_FOLDER=.venv

if [ -d "$VENV_FOLDER" ];then
    echo "VENV $VENV_FOLDER exists."
else
    echo "Creating the VENV $VENV_FOLDER."

    python3 -m venv $VENV_FOLDER --symlinks # --system-site-packages 
    source $VENV_FOLDER/bin/activate
    pip install pytest wheel py-build-cmake
    deactivate
fi


source $VENV_FOLDER/bin/activate

rm -rf build
rm -rf dist
rm -rf .py-build-cmake_cache

pip uninstall viewshed -y
pip install .

# run tests
pytest -vv -s