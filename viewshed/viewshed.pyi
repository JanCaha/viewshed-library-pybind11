#
# AUTOMATICALLY GENERATED FILE, DO NOT EDIT!
#

"""Python interface for viewshed library."""
from __future__ import annotations
import viewshed
import typing

__all__ = [
    "InverseViewshed",
    "Point",
    "ProjectedSquareCellRaster",
    "Viewshed",
    "VisibilityAlgorithms",
    "version",
]


class InverseViewshed:
    """
    Class for calculation of visibility of point.
    """

    def __init__(
        self,
        arg0: Point,
        arg1: float,
        arg2: ProjectedSquareCellRaster,
        arg3: VisibilityAlgorithms,
    ) -> None:
        """
        Create class from target point, observer's offset, dem and visibility indices algorithms.
        """

    @typing.overload
    def calculate(self) -> None:
        """
        Calculate without callbacks.

        Calculate with specified callbacks.
        """

    @typing.overload
    def calculate(
        self,
        arg0: typing.Callable[[str, float], None],
        arg1: typing.Callable[[int, int], None],
    ) -> None:
        ...

    @typing.overload
    def saveResults(self, arg0: str) -> None:
        """
        Store results at specified path.

        Store results at specified pathlib.Path.
        """

    @typing.overload
    def saveResults(self, arg0: object) -> None:
        ...

    def setMaxThreads(self, arg0: int) -> None:
        """
        Set maximum number of threads to use.
        """

    def setVisibilityMask(self, arg0: ProjectedSquareCellRaster) -> None:
        """
        Specifiy visibility mask to use during calculation.
        """

    pass


class Point:
    """
    Point representing either observer or target point.
    """

    def __init__(
        self, arg0: float, arg1: float, arg2: ProjectedSquareCellRaster, arg3: float
    ) -> None:
        """
        Construct using coordinates x,y, ProjectedSquareCellRaster and offset from surface.
        """

    def isValid(self) -> bool:
        """
        Check that point is valid, with respect to provided DEM model.
        """

    pass


class ProjectedSquareCellRaster:
    """
    Class representing raster data.
    """

    @typing.overload
    def __init__(self, arg0: str, arg1: int) -> None:
        """
        Build from string path and  specified band.

        Build from string path.

        Build from pathlib.Path.
        """

    @typing.overload
    def __init__(self, arg0: str) -> None:
        ...

    @typing.overload
    def __init__(self, arg0: object) -> None:
        ...

    def error(self) -> str:
        """
        Error message from the raster.
        """

    def noData(self) -> float:
        """
        NoData value of the raster.
        """

    pass


class Viewshed:
    """
    Class for calculation of visibility from point.
    """

    def __init__(
        self, arg0: Point, arg1: ProjectedSquareCellRaster, arg2: VisibilityAlgorithms
    ) -> None:
        """
        Create class from point, dem and  visibility indices algorithms..
        """

    @typing.overload
    def calculate(self) -> None:
        """
        Calculate without callbacks.

        Calculate with specified callbacks.
        """

    @typing.overload
    def calculate(
        self,
        arg0: typing.Callable[[str, float], None],
        arg1: typing.Callable[[int, int], None],
    ) -> None:
        ...

    @typing.overload
    def saveResults(self, arg0: str) -> None:
        """
        Store results at specified path.

        Store results at specified pathlib.Path.
        """

    @typing.overload
    def saveResults(self, arg0: object) -> None:
        ...

    def setMaxThreads(self, arg0: int) -> None:
        """
        Set maximum number of threads to use.
        """

    def setVisibilityMask(self, arg0: ProjectedSquareCellRaster) -> None:
        """
        Specifiy visibility mask to use during calculation.
        """

    pass


class VisibilityAlgorithms:
    """
    Class for storing visibility indices algorithms.
    """

    @typing.overload
    def __init__(self) -> None:
        """
        Build all algorithms. With default NoData value.

        Build all algorithms with provided NoData value.

        Build only boolean visibility with default NoData value.

        Build only boolean visibility with provided NoData value.
        """

    @typing.overload
    def __init__(self, arg0: float) -> None:
        ...

    @typing.overload
    def __init__(self, arg0: bool) -> None:
        ...

    @typing.overload
    def __init__(self, arg0: bool, arg1: float) -> None:
        ...

    def size(self) -> int:
        ...

    pass


__version__ = "2.7.0"
version = "2.7.0"
