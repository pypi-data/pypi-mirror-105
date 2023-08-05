import pytest

from autofit import database as m
from autofit.mock.mock import Gaussian


@pytest.fixture(
    name="fit"
)
def query_fit(session, paths):
    fit, = m.Fit.all(session)
    return fit


def test_incomplete(paths):
    assert paths.is_complete is False


def test_identifier(
        paths,
        fit
):
    assert fit.id == paths.identifier


def test_completion(
        paths,
        fit
):
    paths.completed()

    assert fit.is_complete
    assert paths.is_complete


def test_object(paths):
    gaussian = Gaussian(
        intensity=2.1
    )

    assert paths.is_object(
        "gaussian"
    ) is False

    paths.save_object(
        "gaussian",
        gaussian
    )

    assert paths.is_object(
        "gaussian"
    ) is True
    assert paths.load_object(
        "gaussian"
    ) == gaussian

    paths.remove_object(
        "gaussian"
    )
    assert paths.is_object(
        "gaussian"
    ) is False


def test_save_all(
        paths,
        fit
):
    paths.save_all({
        "key": "value"
    })

    assert fit.model is not None
    assert "search" in fit
    assert fit.info["key"] == "value"

