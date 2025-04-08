from abc import ABC, abstractmethod

from dask.dataframe import DataFrame


class _ABCFileExporter(ABC):
    @abstractmethod
    def export(self, df: DataFrame, path: str) -> None:
        pass
