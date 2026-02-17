import viewshed


def test_library_version() -> None:
    current_version = "5.0.0"
    assert isinstance(viewshed.version, str)
    assert viewshed.version == current_version
    assert viewshed.__version__ == current_version


def test_algorithms() -> None:
    algs = viewshed.VisibilityAlgorithms(True)
    assert algs.size() == 1

    algs = viewshed.VisibilityAlgorithms(False)
    assert algs.size() == 17
