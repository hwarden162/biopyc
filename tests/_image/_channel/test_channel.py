import dask.array as da
import numpy as np
from numpy import uint8
from pytest import raises

from biopyc._image._channel._channel import Channel


def test_channel_validation():
    with raises(TypeError, match="Image should be a dask array"):
        Channel(1, "Stain")
    with raises(ValueError, match="Image should be of dimension 2"):
        Channel(da.ones((5, 5, 5)), "Stain")
    with raises(TypeError, match="Name should be a string"):
        Channel(da.ones((5, 5)), 1)
    with raises(TypeError, match="Print name should be a string"):
        Channel(da.ones((5, 5)), "Stain", 1)


def test_channel():
    channel = Channel(da.ones((5, 5), dtype=uint8), "Stain", "StainPrintName")
    assert channel.shape == (5, 5)
    assert channel.dtype == uint8
    assert channel.name == "Stain"
    assert channel.print_name == "StainPrintName"
    assert np.array_equal(channel.image.compute(), np.ones((5, 5), dtype=uint8))
    channel = Channel(da.ones((5, 5), dtype=uint8), "Stain")
    assert channel.print_name == "Stain"
