import os
import random

import bpy
from src.main.Module import Module
from src.utility.Utility import Utility


class MountainRandomizer(Module):

    def __init__(self, config):
        Module.__init__(self, config)

    def run(self):

        path = self.config.get_string("path", "")
        mountain_images = os.listdir(path)
  
        chosen = mountain_images[random.randint(0, len(mountain_images)-1)]

        bpy.ops.import_image.to_plane(files=[{"name":chosen, "name":chosen}], directory=path)
        bpy.context.object.name = "Mountain"





