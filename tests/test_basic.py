import shutil
from pathlib import Path

import pytest

import viewshed


def print_val(i, j) -> None:
    print(f"{i}/{j}")


def print_val1(s: str, v: float) -> None:
    print(f"{s}: {v}")


def test_library():
    assert isinstance(viewshed.version, str)
    assert viewshed.version == "2.6.4"


def test_aglorithms():
    algs = viewshed.VisibilityAlgorithms(True)
    assert algs.size() == 1

    algs = viewshed.VisibilityAlgorithms(False)
    assert algs.size() == 17


def test_raster_not_init():
    a = viewshed.ProjectedSquareCellRaster("a.tif")
    assert isinstance(a, viewshed.ProjectedSquareCellRaster)
    assert a.error() == "a.tif: No such file or directory"


def test_point(dem: viewshed.ProjectedSquareCellRaster):
    vp = viewshed.Point(-336428.767, -1189102.785, dem, 1.6)
    assert isinstance(vp, viewshed.Point)
    assert vp.isValid()


def test_invalid_point(dem: viewshed.ProjectedSquareCellRaster):
    vp = viewshed.Point(0, 0, dem, 1.6)
    assert isinstance(vp, viewshed.Point)
    assert vp.isValid() is False


def test_viewshed(
    work_folder: Path,
    dem: viewshed.ProjectedSquareCellRaster,
    viewpoint: viewshed.Point,
):
    algs = viewshed.VisibilityAlgorithms(False)
    v = viewshed.Viewshed(viewpoint, dem, algs)
    assert isinstance(v, viewshed.Viewshed)
    v.calculate()
    v.saveResults(work_folder.as_posix())


def test_inverse_viewshed(work_folder: Path, dem: viewshed.ProjectedSquareCellRaster):
    vp = viewshed.Point(-336428.767, -1189102.785, dem, 0)
    algs = viewshed.VisibilityAlgorithms(False)
    v = viewshed.InverseViewshed(vp, 1.6, dem, algs)
    assert isinstance(v, viewshed.InverseViewshed)
    v.calculate()
    v.saveResults(work_folder.as_posix())
