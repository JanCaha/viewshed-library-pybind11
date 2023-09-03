import shutil
from pathlib import Path

import pytest

import viewshed


@pytest.fixture
def dem_path() -> Path:
    return Path(__file__).parent / "data" / "dsm.tif"


@pytest.fixture
def dem(dem_path: Path) -> viewshed.ProjectedSquareCellRaster:
    dem = viewshed.ProjectedSquareCellRaster(dem_path.as_posix())
    assert isinstance(dem, viewshed.ProjectedSquareCellRaster)
    return dem


@pytest.fixture
def mask_path() -> Path:
    return Path(__file__).parent / "data" / "visiblity_mask.tif"


@pytest.fixture
def mask(mask_path: Path) -> viewshed.ProjectedSquareCellRaster:
    mask = viewshed.ProjectedSquareCellRaster(mask_path.as_posix())
    assert isinstance(mask, viewshed.ProjectedSquareCellRaster)
    return mask


@pytest.fixture
def viewpoint(dem: viewshed.ProjectedSquareCellRaster) -> viewshed.Point:
    vp = viewshed.Point(-336428.767, -1189102.785, dem, 1.6)
    assert vp.isValid()
    return vp


@pytest.fixture
def work_folder() -> Path:
    path = Path("/tmp/test_viewshed")

    if path.exists():
        shutil.rmtree(path)

    path.mkdir(parents=True)

    return path
