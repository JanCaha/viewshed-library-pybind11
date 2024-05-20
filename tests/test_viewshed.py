from pathlib import Path

import viewshed


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

def test_viewshed_visibility_raster(
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

    visibility_raster = work_folder / "visibility_raster.tif"

    v.calculateVisibilityMask()
    v.saveVisibilityRaster(visibility_raster)

    assert visibility_raster.exists()