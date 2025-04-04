from biopyc.image_reader._dask_uint8_image_reader import DaskUInt8ImageReader
from dask.array import Array
from glob import glob
from numpy import array_equal, uint8
from pytest import raises
from skimage.io import imread
from skimage.util import img_as_ubyte

def test_dask_uint8_image_reader_validation(tmpdir):
    image_reader = DaskUInt8ImageReader()
    with raises(TypeError, match="Path should be a string"):
        image_reader.read_image(1)
    with raises(FileNotFoundError, match="Image file not found"):
        image_reader.read_image("./this_file_does_not_exist.txt")
    with raises(IOError, match="Image could not be read by dask image"):
        temp_file = tmpdir.join('testfile.txt')
        temp_file.write("This is a temporary text file for testing.")
        image_reader.read_image(str(temp_file))

def test_dask_uint8_image_reader():
    image_reader = DaskUInt8ImageReader()
    file_list = glob("./tests/imgs/*.tif")
    for file in file_list:
        image = image_reader.read_image(file)
        assert isinstance(image, Array)
        assert image.ndim == 2
        assert image.dtype == uint8
        reference_image = img_as_ubyte(imread(file))
        image_image = image.compute()
        assert array_equal(image_image, reference_image)