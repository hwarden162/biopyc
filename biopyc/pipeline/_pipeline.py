from pandas import DataFrame

from ..file_exporter._abc_file_exporter import _ABCFileExporter
from ..image_reader._abc_image_reader import _ABCImageReader


class Pipeline:
    def __init__(
        self,
        schema: DataFrame,
        image_reader: _ABCImageReader,
        file_exporter: _ABCFileExporter,
    ) -> None:
        """Constructor for the pipeline object

        Args:
            schema (DataFrame): Dataframe to infer the image structure from
            image_reader (_ABCImageReader): Biopyc image reader
            file_exporter (_ABCFileExporter): Biopyc file exporter
        """
        self._infer_inputs_from_schema(schema=schema)
        self._add_image_reader(image_reader=image_reader)
        self._add_file_exporter(file_exporter=file_exporter)

    def _infer_inputs_from_schema(self, schema: DataFrame) -> None:
        """Infer the image structure from image schema

        Args:
            schema (DataFrame): The image schema to infer structure from

        Raises:
            TypeError: If the given input schema is not a pandas dataframe
        """
        if not isinstance(schema, DataFrame):
            raise TypeError("Input schema should be a pandas dataframe")
        column_names = list(schema.columns)
        self.input_intensity_names = [
            name[10:] for name in column_names if name.startswith("Intensity_")
        ]
        self.input_labelmask_names = [
            name[10:] for name in column_names if name.startswith("LabelMask_")
        ]
        self.input_binarymask_names = [
            name[11:] for name in column_names if name.startswith("BinaryMask_")
        ]

    def _add_image_reader(self, image_reader: _ABCImageReader) -> None:
        """Add image reader to the pipeline

        Args:
            image_reader (_ABCImageReader): Image reader to add

        Raises:
            TypeError: The given input is not a Biopyc image reader
        """
        if not isinstance(image_reader, _ABCImageReader):
            raise TypeError("Image reader is not a Biopyc image reader class")
        self.image_reader = image_reader

    def _add_file_exporter(self, file_exporter: _ABCFileExporter) -> None:
        """Add file exporter to the pipeline

        Args:
            file_exporter (_ABCFileExporter): File exporter to add

        Raises:
            TypeError: The given input is not a Biopyc file exporter
        """
        if not isinstance(file_exporter, _ABCFileExporter):
            raise TypeError("File Exporter is not a Biopyc file exporter class")
        self.file_exporter = file_exporter
