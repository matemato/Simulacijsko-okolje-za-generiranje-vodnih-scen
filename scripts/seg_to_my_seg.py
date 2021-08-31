import os

import cv2
import matplotlib.pyplot as plt

path = "../images"

os.chdir(path)

for pic in os.listdir():
    if 'segmap' in pic:
        I = cv2.imread(pic)
        I = I[:,:,0]

        I[I==36] = 0 #obstacle
        I[I==140] = 1 # sea
        I[I==84] = 2 # sky

        name = path + pic 

        cv2.imwrite(name, I)

    if 'imu' in pic:
        I = cv2.imread(pic)
        I = I[:,:,0]

        I[I==0] = 0 #sky
        I[I==1] = 1 # sea

        name = path + pic 

        cv2.imwrite(name, I)
