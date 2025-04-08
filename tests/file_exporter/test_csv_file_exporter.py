import os
from tempfile import TemporaryDirectory

import dask.dataframe as dd
from pandas import DataFrame
from pytest import raises

from biopyc.file_exporter._csv_file_exporter import CSVFileExporter


def test_csv_file_exporter_validation():
    pddf = DataFrame({"Column1": [1, 2, 3], "Column2": [4, 5, 6]})
    df = dd.from_pandas(pddf)
    temp_dir = TemporaryDirectory()
    csv_file_path = os.path.join(str(temp_dir), "test_csv.csv")
    exising_dir = "./tests"
    with raises(TypeError, match="Supplied data is not a dask data frame"):
        CSVFileExporter().export(1, csv_file_path)
    with raises(TypeError, match="Supplied file path is not a string"):
        CSVFileExporter().export(df, 1)
    with raises(FileExistsError, match="Save file already exists"):
        CSVFileExporter().export(df, exising_dir)
