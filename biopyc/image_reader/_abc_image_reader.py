from abc import ABC, abstractmethod
import os

from dask.array import Array


class _ABCImageReader(ABC):
    @abstractmethod
    def read_image(self, path: str) -> Array:
        """Read an image into a dask array

        Args:
            path (str): File path to the image

        Raises:
            TypeError: If the image path is not a string
            FileNotFoundError: If the image path given is not found

        Returns:
            Array: A dask array of the given image
        """        
        if not isinstance(path, str):
            raise TypeError("Path should be a string")
        if not os.path.exists(path):
            raise FileNotFoundError("Image file not found")
