import os

def writeConfigFile(baseDir, configDict, filename="config.txt"):
    os.makedirs(baseDir, exist_ok=True)  # Ensure the directory exists
    file_path = os.path.join(baseDir, filename)
    
    with open(file_path, "w") as f:
        for key, value in configDict.items():
            f.write(f"{key}={value}\n")

def calculateCopies(rectangleAug=False, rectAugFactor=0, geometricAug=False):
    if not rectangleAug and not geometricAug:
        return 
    # If geometric aug only
    if not rectangleAug:
        return 6
    # If rectAug only
    if not geometricAug:
        return rectAugFactor
    
    # Whole suite
    return rectAugFactor * 6

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