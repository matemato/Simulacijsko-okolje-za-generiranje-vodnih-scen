import os

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from src.main.Module import Module


class SegToPngModule(Module):

    def __init__(self, config):
        Module.__init__(self, config)

    def run(self):
        path = self.config.get_string("path", "Diplomska/BlenderProc/Outputs/Output")
        startFrame = self.config.get_int("startFrame", 1)
        endFrame = self.config.get_int("endFrame", 2)

        number_of_images = endFrame - startFrame

        for i in range(number_of_images):
            filename = path + "/segmap_" + str(i+startFrame).zfill(4) + ".npy"
            img_array = np.load(filename, allow_pickle=True)
            img_name = filename[:-4]+".png"
            matplotlib.image.imsave(img_name, img_array)
            os.remove(filename)
