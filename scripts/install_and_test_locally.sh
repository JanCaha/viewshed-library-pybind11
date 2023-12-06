#!/bin/bash
VENV_FOLDER=.venv

if [ -d "$VENV_FOLDER" ];then
    echo "VENV $VENV_FOLDER exists."
else
    echo "Creating the VENV $VENV_FOLDER."

    python3 -m venv $VENV_FOLDER --symlinks # --system-site-packages 
    source $VENV_FOLDER/bin/activate
    pip install pytest wheel
    deactivate
fi

install_viewshed_package(){
    pip uninstall viewshed -y
    pip install .
}

source $VENV_FOLDER/bin/activate

rm -rf build
rm -rf dist

# install the package
install_viewshed_package

# regenerate stub file from installed package
python3 prepare_stub_template.py

# install again with proper stub package
install_viewshed_package

python3 setup.py bdist_wheel

# run tests
pytest -vv -s