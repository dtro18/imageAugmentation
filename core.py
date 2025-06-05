# Core logic for augmentation pipeline
from PIL import Image, ImageEnhance
import os
from pathlib import Path
import random

import utils
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


def geometricAugOfImgArr(imgArr):

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



def rectangleAugOfImgArr(
        images, 
        augFactor, 
        maxWidthProp=0.50, 
        maxHeightProp=0.50, 
        minWidth=50, 
        minHeight=50,
        centerBias=0.0,
        fillColor=0
        ):
    """
    RectangleAugmentation functions as a generator, yielding
    a set of images with a randomized rectangle cropped
    out of the image. Images intended to be black and white;
    Users can specify how many times this operation
    is performed on each image.

    Input:

        images = Array of Image objects
        augFactor = Integer representing how many augmented images produced from one image
        maxWidthProp = Maximum width of image that can be covered, expressed as a decimal proportion
        maxHeightProp = Maximum height of image that can be covered, expressed as a decimal proportion
        minWidth = Minimum width of a rectangle, expressed as pixels
        minHeight = Minimum height of a rectangle, expressed as pixels
        centerBias = Indicates where rectangles should start to cover more of the center of the image. Expressed as decimal.
        fillColor = Scale of 0 to 255, inclusive, ranging from black to white.

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
            x1 = random.randint(int(width * centerBias), width // 2)
            x2 = random.randint(min(x1 + minWidth, width - 1), int(min(x1 + maxWidthProp * width, width - 1)))
            y1 = random.randint(int(height * centerBias), height // 2)
            y2 = random.randint(min(y1 + minHeight, height - 1), int(min(y1 + maxHeightProp * height, height - 1)))
            patch = Image.new("L", (x2 - x1, y2 - y1), fillColor)
            imgCpy = img.copy()
            # Paste it into your original image
            imgCpy.paste(patch, (x1, y1))
            print("Image cropped")
            # imgCpy.show()
            res.append(imgCpy)


        yield res


def increaseContrastOfImgArr(imgArr, contrastFactor=1.0):
    """
    Nullifies pixels below a certain threshold, and increases the brightness of pixels above a certain threshold.

    Input: 

        imgArr = Array of Images (PIL)
        contrastFactor = Factor to increase contrast by; 2.0 doubles the contrast.

    Output: 

        Image array
    """
    # Open image
    res = []

    for img in imgArr:
        # Create an enhancer
        enhancer = ImageEnhance.Contrast(img)

        # Increase contrast (1.0 = original, >1 = more contrast, <1 = less contrast)
        enhanced_img = enhancer.enhance(contrastFactor)  # Doubles the contrast

        res.append(enhanced_img)
    return res

def resizeImgArr(imgArr, size):
    """
    Nullifies pixels below a certain threshold, and increases the brightness of pixels above a certain threshold.

    Input: 

        imgArr = Array of Images (PIL)
        contrastFactor = Factor to increase contrast by; 2.0 doubles the contrast.

    Output: 

        Image array
    """

    res = []
    for img in imgArr:
        res.append(img.resize((size, size)))
    return res


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

# TODO: Test
def initTrialDirectory(
        trialNum,
        baseDir,
        originalImageDir,
        labelImageDir,
        increaseContrast=False,
        contrastFactor=1.0,
        resizeImg=False,
        resizeDim=256,
        rectangleAug=False,
        augFactor=0,
        maxWidthProp=0.50,
        maxHeightProp=0.50, 
        minWidth=50, 
        minHeight=50,
        centerBias=0.0,
        fillColor=0,
        geometricAug=False,
        maxImages=50000
    ):


    """
    Initialize directory containing:

    1) Image folder containing inputs
    2) Label folder
    3) TrialX.txt containing settings applied

    baseDir = Directory to be created to house a trial's data
    originalImagePath = Source directory of input images
    labelImagePath = Source directory of labeled images

    increaseContrast = If image contrast should be increased
    contrastFactor = Factor by which contrast is increased, if increaseContrast = True

    resizeImg = If image should be resized
    resizeDim = Specifies a size of n x n

    rectangleAug = If rectangle augmentation should be applied
    augFactor = Integer representing how many augmented images produced from one image
    maxWidthProp = Maximum width of image that can be covered, expressed as a decimal proportion
    maxHeightProp = Maximum height of image that can be covered, expressed as a decimal proportion
    minWidth = Minimum width of a rectangle, expressed as pixels
    minHeight = Minimum height of a rectangle, expressed as pixels
    centerBias = Indicates where rectangles should start to cover more of the center of the image. Expressed as decimal.
    fillColor = Scale of 0 to 255, inclusive, ranging from black to white.

    geometricAug = If geometric augmentation should be applied

    """
    
    # Initialize config file:
    config = {
        "trialNum": trialNum,
        "baseDir": baseDir,  # Specify your base directory path, containing the results of all the trials/experiments
        "originalImageDir": originalImageDir,  # Specify your original image directory path
        "labelImageDir": labelImageDir,
        "increaseContrast": increaseContrast,
        "contrastFactor": contrastFactor,
        "resizeImg": resizeImg,
        "resizeDim": resizeDim,
        "rectangleAug": rectangleAug,
        "augFactor": augFactor,
        "maxWidthProp": maxWidthProp,
        "maxHeightProp": maxHeightProp,
        "minWidth": minWidth,
        "minHeight": minHeight,
        "centerBias": centerBias,
        "fillColor": fillColor,
        "geometricAug": geometricAug
    }
    utils.writeConfigFile(baseDir, config)


    # Load img/label pairs into Image arrays
    origImgArr = readImageDirIntoArr(originalImageDir)
    labelArr = readImageDirIntoArr(labelImageDir)

    # Calculate the number of copies that would be made
    numCopies = utils.calculateCopies(rectangleAug, augFactor, geometricAug)
    if numCopies * origImgArr > maxImages:
        raise ValueError("Number of images that would be generated is too high. Override with the parameter maxImages.")

    # Make trial, input, and labeled images directories and ensure uniqueness
    trialDirectory = os.path.join(baseDir, "trial_" + str(trialNum))
    os.makedirs(trialDirectory, exist_ok=False)  # Ensure the trial/directory to be created DOES NOT exist
    newInputImagesPath = os.path.join(baseDir, "input_images")
    newLabeledImagesPath = os.path.join(baseDir, "label_images")
    os.makedirs(newInputImagesPath, exist_ok=False)
    os.makedirs(newLabeledImagesPath, exist_ok=False)

    
    # Image Preprocessing Steps
    if resizeImg:
        origImgArr = resizeImgArr(origImgArr, resizeDim)
        labelArr = resizeImgArr(labelArr, resizeDim)
    
    if increaseContrast:
        origImgArr = increaseContrastOfImgArr(origImgArr, contrastFactor)
        # Shouldn't matter for our use case
        labelArr = increaseContrastOfImgArr(labelArr, contrastFactor)

    # Augmentation Steps. Must apply geometric aug first if present
    if geometricAug:
        origImgArr = geometricAugOfImgArr(origImgArr)
        labelArr = geometricAugOfImgArr(labelArr)

    # Apply and save rectangle patch augmentation
    if rectangleAug:
        startIdx = 0
        # Pass in params relating to rectangular augmentation
        for imgArr in rectangleAugOfImgArr(
            origImgArr, augFactor,
            maxWidthProp,
            maxHeightProp, 
            minWidth, 
            minHeight,
            centerBias,
            fillColor
        ):
            saveOutputs(newInputImagesPath, imgArr, startIdx)
            startIdx += len(imgArr)
        
        startIdx = 0
        # For every image in the labeled directory, save n copies (where n = augFactor)
        # One image that had 20 random rectangles patched onto it should have 20 labels.
        for img in labelArr:
            for i in range(augFactor):
                newImgPath = os.path.join(newLabeledImagesPath, str(startIdx).zfill(4) + ".png")
                img.save(newImgPath, format="PNG")
                startIdx += 1
    else:
        startIdx = 0
        saveOutputs(newLabeledImagesPath, labelArr, startIdx)


    # If geometricAug is true, we have to apply the geometric transformation to both sets.

    # Write separate case for geometric xaugmentation, which requires the same tx to be applied to the label set
    # 




# # Read raw images
# arr = readImageDirIntoArr(r"C:\Augmentation\test_images\msk_3_7")
# # Apply geometric augmentation
# arr = rotateReflectAug(arr)
# # Apply contrast filter
# arr = increaseContrast(arr, 3.0)
# # Apply resize
# arr = resizeImgArr(arr, 256)

# # Apply and save rectangle patch augmentation
# startIdx = 0
# for imgArr in rectangleAug(arr, augFactor=10, maxWidthProp=0.70, maxHeightProp=0.70, centerBias=0.20, fillColor=255):
#     saveOutputs(r"C:\Augmentation\test_output", imgArr, startIdx)
#     startIdx += len(imgArr)

