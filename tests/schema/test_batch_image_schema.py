from biopyc.schema._batch_image_schema import batch_image_schema
from pandas import DataFrame
from pytest import raises

def test_batch_image_schema_validation():
    test_df = DataFrame({"Intensity_Stain": ["Image1", "Image2", "Image3", "Image4", "Image5"]})
    with raises(TypeError, match="Given image schema is not a pandas dataframe"):
        batch_image_schema(1, 1)
    with raises(TypeError, match="Batch size is not an integer"):
        batch_image_schema(test_df, "test")
    with raises(ValueError, match="Batch size should be positive"):
        batch_image_schema(test_df, 0)
    with raises(ValueError, match="Given schema has no images in it"):
        batch_image_schema(DataFrame(), 5)

def test_batch_image_schema():
    df = DataFrame({"Intensity_Stain": ["Image1", "Image2", "Image3", "Image4", "Image5"]})
    reference_df = df.copy()
    reference_df["Batch"] = [i for i in range(5)]
    test_df = batch_image_schema(df, 1)
    assert test_df.equals(reference_df)
    