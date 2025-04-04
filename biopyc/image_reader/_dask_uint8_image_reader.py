import os

from dask.array import Array, from_delayed
from dask.delayed import delayed
from dask_image.imread import imread  # type: ignore[import-untyped]
from numpy import ndarray, uint8
from skimage.util import img_as_ubyte

from ._abc_image_reader import _ABCImageReader


class DaskUInt8ImageReader(_ABCImageReader):
    @delayed
    def _convert_to_ubyte(self, image: ndarray) -> ndarray:
        """Convert an image to a ubyte image

        Args:
            image (ndarray): Input image

        Returns:
            ndarray: Output ubyte image
        """
        return img_as_ubyte(image)

    def read_image(self, path: str) -> Array:
        """Read an image as a dask array

        Args:
            path (str): Path to the inpute image

        Raises:
            TypeError: Given file path is not a string
            FileNotFoundError: Image file not found
            IOError: If dask image can't read the image

        Returns:
            Array: The input image as a dask array
        """
        if not isinstance(path, str):
            raise TypeError("Path should be a string")
        if not os.path.exists(path):
            raise FileNotFoundError("Image file not found")
        try:
            image = imread(path)[0, :, :]
        except Exception as e:
            raise IOError(f"Image could not be read by dask image: {e}")
        return from_delayed(
            self._convert_to_ubyte(image), shape=image.shape, dtype=uint8
        )
