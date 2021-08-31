import os
import random
from math import pi, sqrt

import bpy
import numpy as np
from src.main.Module import Module
from src.utility.Utility import Utility


class OceanModule(Module):

    def __init__(self, config):
        Module.__init__(self, config)

    # Sets Subdivision settings in Render Properties    

    def cyclesSubdivision(self):
        bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
        bpy.context.scene.cycles.dicing_rate = 2
        bpy.context.scene.cycles.preview_dicing_rate = 4
        bpy.context.scene.cycles.offscreen_dicing_scale = 10
        bpy.context.scene.render.resolution_x = 512
        bpy.context.scene.render.resolution_y = 384

    # randomization for Ocean A

    def randomizeOcean(self):
        ocean = bpy.data.materials["Ocean"]

        ocean.node_tree.nodes["Mapping.002"].inputs[1].default_value[0] = random.randint(-150, 150)
        ocean.node_tree.nodes["Mapping.002"].inputs[1].default_value[1] = random.randint(-150, 150)

        ocean.node_tree.nodes["Mapping"].inputs[1].default_value[0] = random.randint(-100, 100)
        ocean.node_tree.nodes["Mapping"].inputs[1].default_value[1] = random.randint(-100, 100)

        ocean.node_tree.nodes["Mapping.001"].inputs[1].default_value[0] = random.randint(0, 10000000)
        ocean.node_tree.nodes["Mapping.001"].inputs[1].default_value[1] = random.randint(0, 10000000)

        ocean.node_tree.nodes["Mapping.003"].inputs[1].default_value[0] = random.randint(0, 10000000)
        ocean.node_tree.nodes["Mapping.003"].inputs[1].default_value[1] = random.randint(0, 10000000)

        rotation = random.uniform(0, 2*pi)
        ocean.node_tree.nodes["Mapping"].inputs[2].default_value[2] = rotation
        ocean.node_tree.nodes["Mapping.002"].inputs[2].default_value[2] = rotation

    # randomization for Ocean B

    def oceanModifier(self):
        ocean = bpy.data.objects["ocean tile"]
        ocean.modifiers["Ocean"].random_seed = random.randint(0, 999999999)
        wave_scale = np.random.normal(1.6, 0.7)
        wave_scale = max(0.2, wave_scale)
        ocean.modifiers["Ocean"].wave_scale = wave_scale
        ocean.modifiers["Ocean"].wave_direction = random.uniform(0, 2*pi)
        ocean.modifiers["Ocean"].wave_alignment = random.uniform(0, 1)
        bpy.data.materials["Material"].node_tree.nodes["ColorRamp.002"].color_ramp.elements[0].position = random.uniform(0.55**4, 0.605**4) ** (1/4) # upper foam should be rare, so this function is closer to 0.605
        bpy.data.materials["Material"].node_tree.nodes["ColorRamp.001"].color_ramp.elements[0].position = random.uniform(0.3**4, 0.75**4) ** (1/4) # foam everywhere

        bpy.data.materials["Material"].node_tree.nodes["Mapping.001"].inputs[1].default_value[0] = round(random.uniform(0, 1),3) # randomizes X axis of foam
        bpy.data.materials["Material"].node_tree.nodes["Mapping.001"].inputs[1].default_value[1] = round(random.uniform(0, 1),3) # randomizes Y axis of foam

    # Sets glare and lowers brightness in a special way

    @staticmethod
    def custom_set_denoiser(denoiser):

        if denoiser is None:
            pass
        else:
            # The intel denoiser is activated via the compositor
            bpy.context.scene.use_nodes = True
            nodes = bpy.context.scene.node_tree.nodes
            links = bpy.context.scene.node_tree.links

            # The denoiser gets normal and diffuse color as input
            bpy.context.view_layer.use_pass_normal = True
            # bpy.context.view_layer.use_pass_diffuse_color = True
            bpy.context.view_layer.cycles.denoising_store_passes = True

            # Add denoiser node
            render_layer_node = Utility.get_the_one_node_with_type(nodes, 'CompositorNodeRLayers')
            denoise_node = nodes.new("CompositorNodeDenoise")
            glare_node = nodes.new("CompositorNodeGlare")
            RGB_curves_node = nodes.new("CompositorNodeCurveRGB")
            composite_node = Utility.get_the_one_node_with_type(nodes, 'CompositorNodeComposite')

            # Link nodes

            links.remove(composite_node.inputs[0].links[0])
            
            links.new(render_layer_node.outputs['Image'], denoise_node.inputs['Image'])
            links.new(render_layer_node.outputs['Denoising Albedo'], denoise_node.inputs['Albedo'])
            links.new(render_layer_node.outputs['Normal'], denoise_node.inputs['Normal'])

            links.new(denoise_node.outputs['Image'], glare_node.inputs['Image'])
            links.new(glare_node.outputs['Image'], RGB_curves_node.inputs['Image'])
            links.new(RGB_curves_node.outputs['Image'], composite_node.inputs['Image'])

            # Set Glare node

            glare_node.glare_type = 'FOG_GLOW'
            glare_node.quality = 'HIGH'
            glare_node.mix = -0.95
            glare_node.threshold = 20
            glare_node.size = 6

            # Set RGB node

            RGB_curves_node.mapping.curves[3].points.new(0.25, 0.18)
            RGB_curves_node.mapping.update()

    # sets custom background with z coordinate lowered and brightness lowered    

    @staticmethod
    def custom_set_world_background_hdr_img(path_to_hdr_file):

        path_to_hdr_file = os.getcwd() + "\\" + path_to_hdr_file
        if not os.path.exists(path_to_hdr_file):
            raise Exception("The given path does not exists: {}".format(path_to_hdr_file))

        world = bpy.context.scene.world
        nodes = world.node_tree.nodes
        links = world.node_tree.links

        # add a texture node and load the image and link it
        texture_node = nodes.new(type="ShaderNodeTexEnvironment")
        texture_node.image = bpy.data.images.load(path_to_hdr_file, check_existing=True)

        # get the one output node of the world shader
        output_node = Utility.get_the_one_node_with_type(nodes, "Output")
        background = Utility.get_the_one_node_with_type(nodes, "Background")

        # create 2 new nodes
        mapping = nodes.new(type="ShaderNodeMapping")
        texture_coordinates = nodes.new(type="ShaderNodeTexCoord")

        # link the new texture node to the output
        links.new(texture_node.outputs["Color"], background.inputs["Color"])
        links.new(background.outputs["Background"], output_node.inputs["Surface"])

        links.new(texture_coordinates.outputs["Generated"], mapping.inputs["Vector"])
        links.new(mapping.outputs["Vector"], texture_node.inputs["Vector"])
      
        mapping.inputs[1].default_value[2] = 1.2 # moves the sky down, so it doesn't show hills, mountains...
        mapping.inputs[2].default_value[2] = random.uniform(0, pi*2)
        background.inputs[1].default_value = 5 #random.uniform(1, 5)

    # sets starting and ending frame

    def frameSettings():
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 2

    def run(self):
        self.cyclesSubdivision()

        ocean_type = self.config.get_string("ocean", "OceanA")
        
        if ocean_type == "OceanA":
            self.randomizeOcean() # first ocean
        elif ocean_type == "OceanB":
            self.oceanModifier() #second ocean
        else:
            print("WARNING: Wrong ocean type.")
