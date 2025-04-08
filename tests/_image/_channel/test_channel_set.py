import dask.array as da
from numpy import uint8
from pytest import raises

from biopyc._image._channel._channel import Channel
from biopyc._image._channel._channel_set import (
    BinaryMaskChannelSet,
    ChannelSet,
    IntensityChannelSet,
    LabelMaskChannelSet,
)


def test_channel_set_validation():
    with raises(TypeError, match="Channels should be a channel or a list of channels"):
        ChannelSet(1)
    with raises(ValueError, match="Channel list is empty"):
        ChannelSet([])
    with raises(ValueError, match="All channels should be of the same size"):
        ChannelSet(
            [
                Channel(da.ones((5, 5), dtype=uint8), "Stain1"),
                Channel(da.ones((6, 6), dtype=uint8), "Stain2"),
            ]
        )
    with raises(ValueError, match="All channels should have the same dtype"):
        ChannelSet(
            [
                Channel(da.ones((5, 5), dtype=uint8), "Stain1"),
                Channel(da.ones((5, 5), dtype=int), "Stain2"),
            ]
        )
    with raises(ValueError, match="Channels can't have duplicate names"):
        ChannelSet(
            [
                Channel(da.ones((5, 5), dtype=uint8), "Stain"),
                Channel(da.ones((5, 5), dtype=uint8), "Stain"),
            ]
        )


def test_channel_set():
    channels = [
        Channel(da.ones((5, 5), dtype=uint8), "Stain1"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain2"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain3"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain4"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain5"),
    ]
    channel_set = ChannelSet(channels)
    assert channel_set.channels == channels
    assert channel_set.shape == (5, 5)
    assert channel_set.dtype == uint8


def test_intensity_channel_set_validation():
    with raises(ValueError, match="Dtype of intensities should be numeric"):
        IntensityChannelSet(Channel(da.ones((5, 5), dtype=bool), "Stain"))


def test_intensity_channel_set():
    channels = [
        Channel(da.ones((5, 5), dtype=uint8), "Stain1"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain2"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain3"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain4"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain5"),
    ]
    channel_set = IntensityChannelSet(channels)
    assert channel_set.channels == channels
    assert channel_set.shape == (5, 5)
    assert channel_set.dtype == uint8


def test_label_mask_channel_set_validation():
    with raises(ValueError, match="Dtype of label masks should be an integer"):
        LabelMaskChannelSet(Channel(da.ones((5, 5), dtype=float), "Stain"))


def test_label_mask_channel_set():
    channels = [
        Channel(da.ones((5, 5), dtype=uint8), "Stain1"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain2"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain3"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain4"),
        Channel(da.ones((5, 5), dtype=uint8), "Stain5"),
    ]
    channel_set = LabelMaskChannelSet(channels)
    assert channel_set.channels == channels
    assert channel_set.shape == (5, 5)
    assert channel_set.dtype == uint8


def test_binary_mask_channel_set_validation():
    with raises(ValueError, match="Dtype of binary masks should be boolean"):
        BinaryMaskChannelSet(Channel(da.ones((5, 5), dtype=int), "Stain"))


def test_binary_mask_channel_set():
    channels = [
        Channel(da.ones((5, 5), dtype=bool), "Stain1"),
        Channel(da.ones((5, 5), dtype=bool), "Stain2"),
        Channel(da.ones((5, 5), dtype=bool), "Stain3"),
        Channel(da.ones((5, 5), dtype=bool), "Stain4"),
        Channel(da.ones((5, 5), dtype=bool), "Stain5"),
    ]
    channel_set = BinaryMaskChannelSet(channels)
    assert channel_set.channels == channels
    assert channel_set.shape == (5, 5)
    assert channel_set.dtype == bool
