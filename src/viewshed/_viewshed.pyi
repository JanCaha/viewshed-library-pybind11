"""
Python interface for viewshed library.
"""

from __future__ import annotations
from pathlib import Path
import typing

__all__ = ["InverseViewshed", "Point", "ProjectedSquareCellRaster", "Viewshed", "VisibilityAlgorithms", "version"]

PathLike = typing.Union[str, Path]
StepCallback = typing.Callable[[str, float], None]
PercentCallback = typing.Callable[[int, int], None]

class InverseViewshed:
    """
    Class for calculation of visibility of point.
    """

    def __init__(self, target_point: Point, observer_offset: float, dem: ProjectedSquareCellRaster, algorithms: VisibilityAlgorithms) -> None:
        """
        Create class from target point, observer's offset, dem and visibility indices algorithms.
        """

    @typing.overload
    def calculate(self) -> None:
        """
        Calculate without callbacks.
        """

    @typing.overload
    def calculate(self, stepCallback: StepCallback, percentCallback: PercentCallback) -> None:
        """
        Calculate with specified callbacks.
        """

    def calculateVisibilityMask(self) -> None:
        """
        Calculate visibility mask
        """

    def calculationTime(self) -> float:
        """
        Seconds that processing of last operation lasted.
        """

    @typing.overload
    def saveResults(self, path: str) -> None:
        """
        Store results at specified path.
        """

    @typing.overload
    def saveResults(self, path: PathLike) -> None:
        """
        Store results at specified pathlib.Path.
        """

    def saveVisibilityRaster(self, path: PathLike) -> None:
        """
        Save visibility raster
        """

    def setMaxThreads(self, max_threads: int) -> None:
        """
        Set maximum number of threads to use.
        """

    def setVisibilityMask(self, visibility_mask: ProjectedSquareCellRaster) -> None:
        """
        Specify visibility mask to use during calculation.
        """

class Point:
    """
    Point representing either observer or target point.
    """

    def __init__(self, x: float, y: float, dem: ProjectedSquareCellRaster, offset: float) -> None:
        """
        Construct using coordinates x,y, ProjectedSquareCellRaster and offset from surface.
        """

    def isValid(self) -> bool:
        """
        Check that point is valid, with respect to provided DEM model.
        """

class ProjectedSquareCellRaster:
    """
    Class representing raster data.
    """

    @typing.overload
    def __init__(self, path: str, band: int) -> None:
        """
        Build from string path and  specified band.
        """

    @typing.overload
    def __init__(self, path: str) -> None:
        """
        Build from string path.
        """

    @typing.overload
    def __init__(self, path: PathLike) -> None:
        """
        Build from pathlib.Path.
        """

    def error(self) -> str:
        """
        Error message from the raster.
        """

    def noData(self) -> float:
        """
        NoData value of the raster.
        """

class Viewshed:
    """
    Class for calculation of visibility from point.
    """

    def __init__(self, viewpoint: Point, dem: ProjectedSquareCellRaster, algorithms: VisibilityAlgorithms) -> None:
        """
        Create class from point, dem and  visibility indices algorithms..
        """

    @typing.overload
    def calculate(self) -> None:
        """
        Calculate without callbacks.
        """

    @typing.overload
    def calculate(self, stepCallback: StepCallback, percentCallback: PercentCallback) -> None:
        """
        Calculate with specified callbacks.
        """

    def calculateVisibilityMask(self) -> None:
        """
        Calculate visibility mask
        """

    def calculationTime(self) -> float:
        """
        Seconds that processing of last operation lasted.
        """

    @typing.overload
    def saveResults(self, path: str) -> None:
        """
        Store results at specified path.
        """

    @typing.overload
    def saveResults(self, path: PathLike) -> None:
        """
        Store results at specified pathlib.Path.
        """

    def saveVisibilityRaster(self, path: PathLike) -> None:
        """
        Save visibility raster
        """

    def setMaxThreads(self, max_threads: int) -> None:
        """
        Set maximum number of threads to use.
        """

    def setVisibilityMask(self, visibility_mask: ProjectedSquareCellRaster) -> None:
        """
        Specify visibility mask to use during calculation.
        """

class VisibilityAlgorithms:
    """
    Class for storing visibility indices algorithms.
    """

    @typing.overload
    def __init__(self) -> None:
        """
        Build all algorithms. With default NoData value.
        """

    @typing.overload
    def __init__(self, no_data: float) -> None:
        """
        Build all algorithms with provided NoData value.
        """

    @typing.overload
    def __init__(self, single_visibility_only: bool) -> None:
        """
        Build only boolean visibility with default NoData value.
        """

    @typing.overload
    def __init__(self, single_visibility_only: bool, no_data: float) -> None:
        """
        Build only boolean visibility with provided NoData value.
        """

    def size(self) -> int: ...

