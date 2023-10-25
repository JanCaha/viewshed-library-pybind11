from pathlib import Path

import pytest

import viewshed


def test_library() -> None:
    assert isinstance(viewshed.version, str)
    assert viewshed.version == "2.7.0"


def test_aglorithms() -> None:
    algs = viewshed.VisibilityAlgorithms(True)
    assert algs.size() == 1

    algs = viewshed.VisibilityAlgorithms(False)
    assert algs.size() == 17


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


def test_point(dem: viewshed.ProjectedSquareCellRaster) -> None:
    vp = viewshed.Point(-336428.767, -1189102.785, dem, 1.6)
    assert isinstance(vp, viewshed.Point)
    assert vp.isValid()


def test_invalid_point(dem: viewshed.ProjectedSquareCellRaster) -> None:
    vp = viewshed.Point(0, 0, dem, 1.6)
    assert isinstance(vp, viewshed.Point)
    assert vp.isValid() is False


def test_viewshed(
    work_folder: Path,
    dem: viewshed.ProjectedSquareCellRaster,
    viewpoint: viewshed.Point,
    fn_print_percent_done,
    fn_print_timing,
    file_messages_percent,
    file_messages_timing,
) -> None:
    algs = viewshed.VisibilityAlgorithms(False)

    v = viewshed.Viewshed(viewpoint, dem, algs)
    assert isinstance(v, viewshed.Viewshed)

    v.calculate()

    # alternative call with callback functions that print output
    v.calculate(fn_print_timing, fn_print_percent_done)

    v.saveResults(work_folder.as_posix())
    v.saveResults(work_folder)

    file_messages_percent.seek(0)
    file_messages_timing.seek(0)

    assert len(file_messages_percent.readlines()) == 113967
    assert len(file_messages_timing.readlines()) == 3


def test_inverse_viewshed(
    work_folder: Path,
    dem: viewshed.ProjectedSquareCellRaster,
    fn_print_percent_done,
    fn_print_timing,
    file_messages_percent,
    file_messages_timing,
) -> None:
    algs = viewshed.VisibilityAlgorithms(False)

    tp = viewshed.Point(-336428.767, -1189102.785, dem, 0)

    iv = viewshed.InverseViewshed(tp, 1.6, dem, algs)
    assert isinstance(iv, viewshed.InverseViewshed)

    iv.calculate()

    # alternative call with callback functions that print output
    iv.calculate(fn_print_timing, fn_print_percent_done)

    iv.saveResults(work_folder.as_posix())
    iv.saveResults(work_folder)

    file_messages_percent.seek(0)
    file_messages_timing.seek(0)

    assert len(file_messages_percent.readlines()) == 189945
    assert len(file_messages_timing.readlines()) == 3


def test_viewshed_mask(
    work_folder: Path,
    dem: viewshed.ProjectedSquareCellRaster,
    viewpoint: viewshed.Point,
    mask: viewshed.ProjectedSquareCellRaster,
    fn_print_percent_done,
    fn_print_timing,
    file_messages_percent,
    file_messages_timing,
) -> None:
    algs = viewshed.VisibilityAlgorithms(False)

    v = viewshed.Viewshed(viewpoint, dem, algs)
    assert isinstance(v, viewshed.Viewshed)

    v.setVisibilityMask(mask)

    v.calculate()

    # alternative call with callback functions that print output
    v.calculate(fn_print_timing, fn_print_percent_done)

    v.saveResults(work_folder.as_posix())
    v.saveResults(work_folder)

    file_messages_percent.seek(0)
    file_messages_timing.seek(0)

    assert len(file_messages_percent.readlines()) == 84419
    assert len(file_messages_timing.readlines()) == 3
