# Python Package for viewshed C++ library

Minimalistic python interface for C++ library [viewshed](https://github.com/JanCaha/cpp-viewshed-library). Makes running examples and experiments much easier.

## Running from Python

### Viewshed

```python
from pathlib import Path
import viewshed

# folder to store results in
result_folder = Path("path/to/folder/")

# load first band of file as DEM 
dem = viewshed.ProjectedSquareCellRaster(Path("path/to/file.ext"))

# create viewpoint at coordinates (1, 2) on DEM raster with observer offset 1.6
vp = viewshed.Point(1, 2, dem, 1.6)

# prepare all visibility indices algorithms with and set noData value from DEM as noData to results
algs = viewshed.VisibilityAlgorithms(dem.noData())

# prepare viewshed for calculation with viewpoint, dem and algorithms
v = viewshed.Viewshed(vp, dem, algs)

# optionally max usable threads for calculation can be set with, otherwise all available threads are used
# v.setMaxThreads(4) 

# run the calculation
v.calculate()

# save result rasters in folder
v.saveResults(result_folder)
```

### InverseViewshed

```python
from pathlib import Path
import viewshed

# folder to store results in
result_folder = Path("path/to/folder/")

# load first band of file as DEM 
dem = viewshed.ProjectedSquareCellRaster(Path("path/to/file.ext"))

# create viewpoint at coordinates (1, 2) on DEM raster with observer offset 1.6
tp = viewshed.Point(1, 2, dem, 0.0)

# prepare all visibility indices algorithms with and set noData value from DEM as noData to results
algs = viewshed.VisibilityAlgorithms(dem.noData())

# prepare viewshed for calculation with viewpoint, observer offset, dem and algorithms
iv = viewshed.InverseViewshed(tp, 1.6, dem, algs)

# optionally max usable threads for calculation can be set with, otherwise all available threads are used
# iv.setMaxThreads(4) 

# run the calculation
iv.calculate()

# save result rasters in folder
iv.saveResults(result_folder)
```
