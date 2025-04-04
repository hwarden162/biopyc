from biopyc.schema._create_image_schema import create_image_schema
from pytest import raises
from tempfile import TemporaryDirectory

def test_create_image_schema_validation():
    with raises(TypeError, match="Input folder should be a string"):
        create_image_schema(1)
    with raises(FileNotFoundError, match="Input folder can't be found"):
        create_image_schema("./this_file_does_not_exist.txt")
    with raises(TypeError, match="Pattern should be a string"):
        create_image_schema("./tests/imgs", 2)
    with raises(TypeError, match="Recursive should be a boolean value"):
        create_image_schema("./tests/imgs", recursive=1)
    with raises(TypeError, match="Meta func should be callable"):
        create_image_schema("./tests/imgs", meta_func=1)
    with raises(TypeError, match="Exclusion strings should be a list"):
        create_image_schema("./tests/imgs", exclusion_strings=1)
    with raises(TypeError, match="Every entry of exclusion strings should be a string"):
        create_image_schema("./tests/imgs", exclusion_strings=["hello", 1])
    with raises(FileNotFoundError, match="No input images found"):
        with TemporaryDirectory() as empty_dir:
            create_image_schema(str(empty_dir))
    with raises(ValueError, match="All files contain a string to exclude"):
        create_image_schema("./tests/imgs", exclusion_strings=[".tif"])
