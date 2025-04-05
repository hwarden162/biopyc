from biopyc.schema._create_image_schema import create_image_schema
from glob import glob
from pandas import concat, DataFrame
from pathlib import Path
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

def test_create_image_schema():
    # Test basic usage
    image_file_paths = glob(str(Path("./tests/imgs/*.tif").resolve()))
    reference_df = DataFrame({"Image_Intensity": image_file_paths})
    test_df = create_image_schema("./tests/imgs", "*.tif")
    assert test_df.equals(reference_df)
    # Test Exclusion
    image_file_paths = glob(str(Path("./tests/imgs/*.tif").resolve()))
    image_file_paths = [image_file_path for image_file_path in image_file_paths if not "w5" in image_file_path]
    reference_df = DataFrame({"Image_Intensity": image_file_paths})
    test_df = create_image_schema("./tests/imgs", "*.tif", exclusion_strings=["w5"])
    assert test_df.equals(reference_df)
    
    def image_meta_func(filename):
        filename = Path(filename).name.split("_")
        rename_dict = {"w1": "Image_Nuclei", "w2": "Image_ER", "w3": "Image_CytoRNA", "w4": "Image_AGP", "w5": "Image_Mito"}
        return {
            "Plate": filename[0],
            "Row": filename[1][0],
            "Column": filename[1][1:],
            "Site": filename[2][1:],
            "Stain": rename_dict[filename[3][:-4]]
        }
    
    image_file_paths = glob(str(Path("./tests/imgs/*.tif").resolve()))
    reference_dfs = []
    for image in image_file_paths:
        meta_dict = image_meta_func(image)
        meta_dict = {
            f"Metadata_{key}" if not key.startswith("Metadata_") else key: value
            for key, value in meta_dict.items()
        }
        meta_dict["Image_Intensity"] = image
        reference_dfs.append(DataFrame(meta_dict, index=[0]))
    reference_df = concat(reference_dfs).reset_index(drop=True)
    test_df = create_image_schema("./tests/imgs", "*.tif", meta_func=image_meta_func)
    assert test_df.equals(reference_df)