pip uninstall viewshed
rm -rf build
rm -rf dist

python3 setup.py bdist_wheel
pip install dist/viewshed-*.whl # --force-reinstall

pytest -vv -s