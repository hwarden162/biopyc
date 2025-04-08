from pandas import DataFrame


def batch_image_schema(schema: DataFrame, batch_size: int) -> DataFrame:
    if not isinstance(schema, DataFrame):
        raise TypeError("Given image schema is not a pandas dataframe")
    if not isinstance(batch_size, int):
        raise TypeError("Batch size is not an integer")
    if batch_size <= 0:
        raise ValueError("Batch size should be positive")
    num_images = len(schema)
    if not num_images > 0:
        raise ValueError("Given schema has no images in it")
    batches = [i // batch_size for i in range(num_images)]
    schema["Batch"] = batches
    return schema
