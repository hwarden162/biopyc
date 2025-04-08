from typing import Optional

from ._channel._channel_set import (
    BinaryMaskChannelSet,
    IntensityChannelSet,
    LabelMaskChannelSet,
)


class BiopycImage:
    def __init__(
        self,
        intensities: Optional[IntensityChannelSet] = None,
        label_masks: Optional[LabelMaskChannelSet] = None,
        binary_masks: Optional[BinaryMaskChannelSet] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        if intensities is not None and not isinstance(intensities, IntensityChannelSet):
            raise TypeError("Intensities should be an IntensityChannelSet")
        if label_masks is not None and not isinstance(label_masks, LabelMaskChannelSet):
            raise TypeError("Label masks should be a LabelMaskChannelSet")
        if binary_masks is not None and not isinstance(
            binary_masks, BinaryMaskChannelSet
        ):
            raise TypeError("Binary masks should be a BinaryMaskChannelSet")
        if metadata is not None and not isinstance(metadata, dict):
            raise TypeError("metadata should be a dictionary")
        self.intensities = intensities
        self.label_masks = label_masks
        self.binary_masks = binary_masks
        self.metadata = metadata
