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