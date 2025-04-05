from typing import Optional

from dask.array import Array


class Channel:
    def __init__(
        self, image: Array, name: str, print_name: Optional[str] = None
    ) -> None:
        if not isinstance(image, Array):
            raise TypeError("Image should be a dask array")
        if not image.ndim == 2:
            raise ValueError("Image should be of dimension 2")
        if not isinstance(name, str):
            raise TypeError("Name should be a string")
        if print_name is not None:
            if not isinstance(print_name, str):
                raise TypeError("Print name should be a string")
        else:
            print_name = name
        self.image = image
        self.shape = image.shape
        self.dtype = image.dtype
        self.name = name
        self.print_name = print_name
