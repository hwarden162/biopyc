import dask.array as da
from numpy import uint8
from pytest import raises

from biopyc._image._biopyc_image import BiopycImage
from biopyc._image._channel._channel import Channel
from biopyc._image._channel._channel_set import (
    BinaryMaskChannelSet,
    IntensityChannelSet,
    LabelMaskChannelSet,
)


def test_biopyc_image_validation():
    intensity_channel_set = IntensityChannelSet(
        [Channel(da.ones((5, 5), dtype=uint8), "Stain1")]
    )
    label_mask_channel_set = LabelMaskChannelSet(
        [Channel(da.ones((5, 5), dtype=uint8), "Stain1")]
    )
    binary_mask_channel_set = BinaryMaskChannelSet(
        [Channel(da.ones((5, 5), dtype=bool), "Stain1")]
    )
    with raises(TypeError, match="Intensities should be an IntensityChannelSet"):
        BiopycImage(1)
    with raises(TypeError, match="Label masks should be a LabelMaskChannelSet"):
        BiopycImage(intensity_channel_set, 1)
    with raises(TypeError, match="Binary masks should be a BinaryMaskChannelSet"):
        BiopycImage(intensity_channel_set, label_mask_channel_set, 1)
    with raises(TypeError, match="metadata should be a dictionary"):
        BiopycImage(
            intensity_channel_set, label_mask_channel_set, binary_mask_channel_set, 1
        )


def test_biopyc_image():
    intensity_channel_set = IntensityChannelSet(
        [Channel(da.ones((5, 5), dtype=uint8), "Stain1")]
    )
    label_mask_channel_set = LabelMaskChannelSet(
        [Channel(da.ones((5, 5), dtype=uint8), "Stain1")]
    )
    binary_mask_channel_set = BinaryMaskChannelSet(
        [Channel(da.ones((5, 5), dtype=bool), "Stain1")]
    )
    metadata = {"Metadata_1": 1, "Metadata_2": "Information"}
    bimg = BiopycImage(
        intensity_channel_set, label_mask_channel_set, binary_mask_channel_set, metadata
    )
    assert bimg.intensities == intensity_channel_set
    assert bimg.label_masks == label_mask_channel_set
    assert bimg.binary_masks == binary_mask_channel_set
    assert bimg.metadata == metadata
