import unittest
from imageaugmentationpipeline import core

class UnitTests(unittest.TestCase):
    def test_noise_reduce(self):
        imgArr = core.readImageDirIntoArr(r"C:\augmentation\test_projects\test_images_src")
        imgArr[0].show()
        imgArr = core.reduceNoise(imgArr, 75)
        imgArr[0].show()

    def test_contrast(self):
        imgArr = core.readImageDirIntoArr(r"C:\augmentation\test_projects\test_images_src")
        imgArr[0].show()
        imgArr = core.increaseContrastOfImgArr(imgArr, 3.0)
        imgArr[0].show()

    def test_img_resize(self):
        imgArr = core.readImageDirIntoArr(r"C:\augmentation\test_projects\test_images_src")
        imgArr[0].show()
        imgArr = core.resizeImgArr(imgArr, 256)
        imgArr[0].show()
# Why is this line necessary?
if __name__ == '__main__':
    unittest.main()