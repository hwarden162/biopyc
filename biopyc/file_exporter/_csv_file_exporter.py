import os

from dask.dataframe import DataFrame

from ._abc_file_exporter import _ABCFileExporter


class CSVFileExporter(_ABCFileExporter):
    def export(self, df: DataFrame, path: str) -> None:
        if not isinstance(df, DataFrame):
            raise TypeError("Supplied data is not a dask data frame")
        if not isinstance(path, str):
            raise TypeError("Supplied file path is not a string")
        if os.path.exists(path):
            raise FileExistsError("Save file already exists")
        df.to_csv(path, index=False, single_file=True)
