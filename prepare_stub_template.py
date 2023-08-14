from pybind11_stubgen import ModuleStubsGenerator

module = ModuleStubsGenerator("viewshed")
module.parse()
module.write_setup_py = True

with open("viewshed/viewshed.pyi", "w") as fp:
    fp.write("#\n# AUTOMATICALLY GENERATED FILE, DO NOT EDIT!\n#\n\n")
    fp.write("\n".join(module.to_lines()))
