from pathlib import Path

import viewshed


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
