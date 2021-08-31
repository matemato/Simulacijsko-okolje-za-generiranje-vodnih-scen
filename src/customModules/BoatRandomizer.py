import os
import random

import bpy
from src.main.Module import Module
from src.utility.Utility import Utility


class BoatRandomizer(Module):

    def __init__(self, config):
        Module.__init__(self, config)

    def run(self):

        boats = self.config.get_int("boats", 1)
        boats = round(random.uniform(0, boats**(1/4)) ** 4)
        boats_close = self.config.get_int("boats_close", 1)
        path = self.config.get_string("path", "")

        boat_images = os.listdir(path)

        for i in range(boats):    
            chosen = boat_images[random.randint(0, len(boat_images)-1)]
            bpy.ops.import_image.to_plane(files=[{"name":chosen, "name":chosen}], directory=path)
            bpy.context.object.name = "Boat" + str(i)

        for i in range(boats_close):    
            chosen = boat_images[random.randint(0, len(boat_images)-1)]
            bpy.ops.import_image.to_plane(files=[{"name":chosen, "name":chosen}], directory=path)
            bpy.context.object.name = "Boat_close" + str(i)





