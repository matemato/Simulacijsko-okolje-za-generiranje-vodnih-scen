import os
import random

import bpy
from src.main.Module import Module
from src.utility.Utility import Utility


class BuoyRandomizer(Module):

    def __init__(self, config):
        Module.__init__(self, config)

    def run(self):

        buoys = self.config.get_int("buoys", 1)
        buoys = round(random.uniform(0, buoys**(1/4)) ** 4)
        buoys_close = self.config.get_int("buoys_close", 1)
        path = self.config.get_string("path", "")

        buoy_images = os.listdir(path)

        for i in range(buoys):    
            chosen = buoy_images[random.randint(0, len(buoy_images)-1)]
            bpy.ops.import_image.to_plane(files=[{"name":chosen, "name":chosen}], directory=path)
            bpy.context.object.name = "Buoy" + str(i)

        for i in range(buoys_close):    
            chosen = buoy_images[random.randint(0, len(buoy_images)-1)]
            bpy.ops.import_image.to_plane(files=[{"name":chosen, "name":chosen}], directory=path)
            bpy.context.object.name = "Buoy_close" + str(i)
