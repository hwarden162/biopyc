from typing import List

from numpy import bool_, integer, issubdtype, number

from ._channel import Channel


class ChannelSet:
    def __init__(self, channels: List[Channel] | Channel) -> None:
        if isinstance(channels, Channel):
            channels = [channels]
        if not isinstance(channels, list):
            raise TypeError("Channels should be a channel or a list of channels")
        if len(channels) == 0:
            raise ValueError("Channel list is empty")
        reference_channel = channels[0]
        if not all([reference_channel.shape == channel.shape for channel in channels]):
            raise ValueError("All channels should be of the same size")
        if not all([reference_channel.dtype == channel.dtype for channel in channels]):
            raise ValueError("All channels should have the same dtype")
        channel_names = [channel.name for channel in channels]
        if len(channel_names) != len(set(channel_names)):
            raise ValueError("Channels can't have duplicate names")
        self.channels = channels
        self.shape = reference_channel.shape
        self.dtype = reference_channel.dtype


class IntensityChannelSet(ChannelSet):
    def __init__(self, channels) -> None:
        super().__init__(channels)
        if not issubdtype(self.dtype, number):
            raise ValueError("Dtype of intensities should be numeric")


class LabelMaskChannelSet(ChannelSet):
    def __init__(self, channels) -> None:
        super().__init__(channels)
        if not issubdtype(self.dtype, integer):
            raise ValueError("Dtype of label masks should be an integer")


class BinaryMaskChannelSet(ChannelSet):
    def __init__(self, channels) -> None:
        super().__init__(channels)
        if not issubdtype(self.dtype, bool_):
            raise ValueError("Dtype of binary masks should be boolean")
