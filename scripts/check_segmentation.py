import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

path = imgPath = "../images"

os.chdir(path)

for pic in os.listdir():
    if 'segmap' in pic:
        I = cv2.imread(pic)
        I = I[:,:,0]
        if len(np.unique(I)) < 3:
            print(pic)
            print(len(np.unique(I)))