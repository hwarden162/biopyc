import os
from tempfile import TemporaryDirectory

import dask.dataframe as dd
from pandas import DataFrame, read_csv
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


def test_csv_file_exporter(tmpdir):
    df = dd.from_pandas(DataFrame({"Column1": [1, 2, 3], "Column2": [4, 5, 6]}))
    file_path = tmpdir.join("test_csv.csv")
    CSVFileExporter().export(df, str(file_path))
    assert file_path.exists()
    test_df = read_csv(str(file_path))
    assert test_df.equals(df.compute())
