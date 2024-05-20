import black
from pybind11_stubgen import ModuleStubsGenerator

module = ModuleStubsGenerator("viewshed")
module.parse()
module.write_setup_py = True

path = "viewshed/viewshed.pyi"

with open(path, "w") as fp:
    fp.write("#\n# AUTOMATICALLY GENERATED FILE, DO NOT EDIT!\n#\n\n")
    lines = "\n".join(module.to_lines())
    formatted = black.format_str(lines, mode=black.FileMode())
    fp.write(formatted)


print("Done!")
