import os
from glob import glob
from pathlib import Path
from typing import Callable, List, Optional

from pandas import DataFrame, concat


def create_image_schema(
    input_folder: str,
    pattern: str = "*",
    recursive: bool = False,
    meta_func: Optional[Callable] = None,
    exclusion_strings: List[str] = [],
) -> DataFrame:
    if not isinstance(input_folder, str):
        raise TypeError("Input folder should be a string")
    if not os.path.exists(input_folder):
        raise FileNotFoundError("Input folder can't be found")
    if not isinstance(pattern, str):
        raise TypeError("Pattern should be a string")
    if not isinstance(recursive, bool):
        raise TypeError("Recursive should be a boolean value")
    if meta_func is not None and not callable(meta_func):
        raise TypeError("Meta func should be callable")
    if not isinstance(exclusion_strings, list):
        raise TypeError("Exclusion strings should be a list")
    if len(exclusion_strings) > 0:
        if not all([isinstance(string, str) for string in exclusion_strings]):
            raise TypeError("Every entry of exclusion strings should be a string")
    abs_input_pattern = os.path.join(str(Path(input_folder).resolve()), pattern)
    input_images = glob(abs_input_pattern, recursive=recursive)
    if len(input_images) == 0:
        raise FileNotFoundError("No input images found")
    if len(exclusion_strings) > 0:
        input_images = [
            image
            for image in input_images
            if not any(excl in image for excl in exclusion_strings)
        ]
    if len(input_images) == 0:
        raise ValueError("All files contain a string to exclude")
    if meta_func is None:
        return DataFrame({"Image_Intensity": input_images})
    dfs = []
    for image in input_images:
        meta_dict = meta_func(image)
        meta_dict["Image_Intensity"] = image
        dfs.append(DataFrame(meta_dict))
    return concat(dfs)
