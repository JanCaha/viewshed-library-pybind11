from pathlib import Path

import pytest

import viewshed


def test_raster_paths_init() -> None:
    with pytest.raises(RuntimeError) as e:
        a = viewshed.ProjectedSquareCellRaster(123)
    assert "must be PurePath" in str(e)

    a = viewshed.ProjectedSquareCellRaster(Path("a.tif"))
    assert isinstance(a, viewshed.ProjectedSquareCellRaster)
    assert a.error() == "a.tif: No such file or directory"


def test_raster_not_init() -> None:
    a = viewshed.ProjectedSquareCellRaster("a.tif")
    assert isinstance(a, viewshed.ProjectedSquareCellRaster)
    assert a.error() == "a.tif: No such file or directory"
