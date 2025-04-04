from abc import ABC, abstractmethod

from dask.array import Array


class _ABCImageReader(ABC):
    @abstractmethod
    def read_image(self, path: str) -> Array:
        """Abstract method to read an image

        Args:
            path (str): File location of image

        Returns:
            Array: Dask array of the image
        """
        pass
