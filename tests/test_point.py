import viewshed


def test_point(dem: viewshed.ProjectedSquareCellRaster) -> None:
    vp = viewshed.Point(-336428.767, -1189102.785, dem, 1.6)
    assert isinstance(vp, viewshed.Point)
    assert vp.isValid()


def test_invalid_point(dem: viewshed.ProjectedSquareCellRaster) -> None:
    vp = viewshed.Point(0, 0, dem, 1.6)
    assert isinstance(vp, viewshed.Point)
    assert vp.isValid() is False
