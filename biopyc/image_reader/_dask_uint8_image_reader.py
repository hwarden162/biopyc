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
    
    def read_image(self, path) -> Array:
        """Read an image as a dask array

        Args:
            path (_type_): Path to the inpute image

        Raises:
            IOError: If dask image can't read the image

        Returns:
            Array: The input image as a dask array
        """        
        super().read_image(path)
        try:
            image = imread(path)[0, :, :]
        except:
            raise IOError("Image could not be read by dask image")
        return from_delayed(
            self._convert_to_ubyte(image), shape=image.shape, dtype=uint8
        )