import unittest
from imageaugmentationpipeline import core

class IntegrationTests(unittest.TestCase):
    def test_init_trial_directory(self):
        core.initTrialDirectory(
            1,
            r"C:\augmentation\test_projects",
            r"C:\augmentation\test_projects\test_images_src",
            r"C:\augmentation\test_projects\test_label_src",
            increaseContrast=True,
            contrastFactor=2.0,
            resizeImg=True,
            resizeDim=256,
            rectangleAug=True,
            augFactor=10,
            maxWidthProp=0.70,
            maxHeightProp=0.70,
            minWidth=50,
            minHeight=50,
            centerBias=0.0,
            fillColor=0,
            geometricAug=True
        )

    def test_image_processing_suite(self):
        imgArr = core.readImageDirIntoArr(r"C:\augmentation\test_projects\test_images_src")
        imgArr[0].show()
        imgArr = core.reduceNoise(imgArr, 75)
        imgArr = core.increaseContrastOfImgArr(imgArr, 3.0)
        imgArr = core.resizeImgArr(imgArr, 256)
        imgArr[0].show()


if __name__ == '__main__':
    unittest.main()