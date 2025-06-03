# Core logic for augmentation pipeline
from PIL import Image, ImageEnhance
import os
from pathlib import Path
import random
# Params
# IMAGE_INPUT_DIR = File directory containing images to be augmented
# AUGMENTATION_TYPE = randomcrop, rotation, reflection

'''
Opens and reads an image directory into an array of Image objects (PIL)
Input: string filePath 
Output: array of Images
'''
def readImageDirIntoArr(filePath):
    files = os.listdir(Path(filePath))
    imgArr = []
    for fileName in files:
        fullPath = os.path.join(filePath, fileName)
        imgArr.append(Image.open(fullPath))
    return imgArr


def rotateReflectAug(imgArr):

    """
    Applies five geometric transformations, including rotation and reflection
    on a specified array of Images.
    Input: Array of Image (PIL) objects
    Output: Array of original images plus their transformations (5 each).

    """
    newImgArr = []

    for img in imgArr:
        transformations = [
            img,  # Original
            img.transpose(Image.FLIP_LEFT_RIGHT),  # Flip X
            img.transpose(Image.FLIP_TOP_BOTTOM),  # Flip Y
            img.transpose(Image.ROTATE_90),  # Rotate 90°
            img.transpose(Image.ROTATE_180),  # Rotate 180°
            img.transpose(Image.ROTATE_270)  # Rotate 270°
        ]
        for transformedImage in transformations:
            newImgArr.append(transformedImage)
    return newImgArr



def rectangleAug(
        images, 
        augFactor, 
        maxWidthProp=1.00, 
        maxHeightProp=1.00, 
        minWidth=50, 
        minHeight=50,
        centerBias=0.0
        ):
    """
    RectangleAugmentation functions as a generator, yielding
    a set of images with a randomized rectangle cropped
    out of the image. Users can specify how many times this operation
    is performed on each image.

    Input:

        images = Array of Image objects
        augFactor = Integer representing how many augmented images produced from one image
        maxWidthProp = Maximum width of image that can be covered, expressed as a decimal proportion
        maxHeightProp = Maximum height of image that can be covered, expressed as a decimal proportion
        minWidth = Minimum width of a rectangle, expressed as pixels
        minHeight = Minimum height of a rectangle, expressed as pixels
        centerBias = Indicates where rectangles should start to cover more of the center of the image. Expressed as decimal.

    Yields:

        An array of augmented images generated from one original image.

    """
    if images == None:
        print("No images")
        return False
    
    for img in images:
        res = []
        width, height = img.size
        for i in range(augFactor):
            x1 = random.randint(int(width * centerBias), width - 1)
            x2 = random.randint(min(x1 + minWidth, width - 1), int(min(x1 + maxWidthProp * width, width - 1)))
            y1 = random.randint(int(height * centerBias), height - 1)
            y2 = random.randint(min(y1 + minHeight, height - 1), int(min(y1 + maxHeightProp * height, height - 1)))
            patch = Image.new("L", (x2 - x1, y2 - y1), 255)
            imgCpy = img.copy()
            # Paste it into your original image
            imgCpy.paste(patch, (x1, y1))
            print("Image cropped")
            # imgCpy.show()
            res.append(imgCpy)


        yield res


def increaseContrast(imgArr, contrastFactor=1.0):
    """
    Nullifies pixels below a certain threshold, and increases the brightness of pixels above a certain threshold.

    Input: 

        imgArr = Array of Images (PIL)
        contrastFactor = Factor to increase contrast by; 2.0 doubles the contrast.

    Output: 

        Image array
    """
    # Open image
    for img in imgArr:
        img.show()
        # Create an enhancer
        enhancer = ImageEnhance.Contrast(img)

        # Increase contrast (1.0 = original, >1 = more contrast, <1 = less contrast)
        enhanced_img = enhancer.enhance(3.0)  # Doubles the contrast

        # Save or show the result
        enhanced_img.show()


def saveOutputs(outputDir, augArr, startIdx):

    """
    Saving function that saves an array of Image objects to a specified directory. This names
    images sequentially e.g. 0000.png, 0001.png, etc.

        Inputs: 
            outputDir = String format; this will be created if it doesn't exist.
            augArr = An array containing the augmentations of one image.
            startIdx = Indicates at what number where naming will begin.

        Returns: 
            None
    """
    os.makedirs(outputDir, exist_ok=True)
    for img in augArr:
        newImgPath = os.path.join(outputDir, str(startIdx).zfill(4) + ".png")
        img.save(newImgPath, format="PNG")
        startIdx += 1
    print(f"Image saved to: {newImgPath}")


# # Read raw images
arr = readImageDirIntoArr(r"C:\imageAugmentation\test_images")
# # Apply geometric augmentation
# arr = rotateReflectAug(arr)

# # Apply and save rectangle patch augmentation
# startIdx = 0
# for imgArr in rectangleCropAug(arr, augFactor=10, maxWidthProp=0.70, maxHeightProp=0.70):
#     saveOutputs(r"C:\imageAugmentation\test_output", imgArr, startIdx)
#     startIdx += len(imgArr)

increaseContrast(arr, 3.0)