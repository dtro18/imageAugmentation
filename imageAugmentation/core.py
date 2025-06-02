# Core logic for augmentation pipeline
from PIL import Image
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

'''
rectangleCrop functions as a generator, yielding
a set of images with a randomized rectangle cropped
out of the image.
Input:
images = Array of Image objects
bw = True/False
format = png/bmp
replaceColor = black/white
augFactor = Integer representing how many augmented images produced from one image
maxWidthProp = Maximum width of image that can be covered, expressed as a decimal
maxHeightProp = Maximum height of image that can be covered, expressed as a decimal
minWidth = Minimum width of a rectangle, expressed as pixels
minHeight = Minimum height of a rectangle, expressed as pixels
centerBias = Indicates where rectangles should start to cover more of the center of the image. Expressed as decimal.

'''
def rectangleCrop(
        images, 
        augFactor, 
        bw=True, 
        format="png", 
        replaceColor="blk", 
        maxWidthProp=1.00, 
        maxHeightProp=1.00, 
        minWidth=50, 
        minHeight=50,
        centerBias=0.0
        ):
    if images == None:
        print("No images")
        return False
    
    for img in images:
        res = []
        width, height = img.size
        maxWidth, maxHeight = width * maxWidthProp, height * maxHeightProp
        for i in range(augFactor):
            x1 = random.randint(int(width * centerBias), width - 1)
            x2 = random.randint(min(x1 + minWidth, width - 1), int(min(x1 + maxWidthProp * width, width - 1)))
            y1 = random.randint(int(height * centerBias), height - 1)
            y2 = random.randint(min(y1 + minHeight, height - 1), int(min(y1 + maxHeightProp * height, height - 1)))

                        # Make a noise patch, or get any other region
            patch = Image.new("L", (x2 - x1, y2 - y1), 255)
            imgCpy = img.copy()
            # Paste it into your original image
            imgCpy.paste(patch, (x1, y1))
            print("Image cropped")
            # imgCpy.show()
            res.append(imgCpy)


        yield res
'''
Inputs: 
outputDir = String format; will be created if it doesn't exist.
augArr = An array containing the augmentations of one image.
startIdx = Indicates where naming will begin

Returns: None
'''
def saveOutputs(outputDir, augArr, startIdx):
    os.makedirs(outputDir, exist_ok=True)
    for img in augArr:
        newImgPath = os.path.join(outputDir, str(startIdx).zfill(4) + ".png")
        img.save(newImgPath, format="PNG")
        startIdx += 1
    print(f"Image saved to: {newImgPath}")

