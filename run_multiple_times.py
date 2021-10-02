import argparse
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--config_file', help="Path to config.yaml.", default="ocean/OceanB/debug.yaml")
parser.add_argument('--cam_file', help="Path to camera positions.", default="ocean/OceanB/camera_position")
parser.add_argument('--blend_file', help="Path to .blend file.", default="ocean/OceanB/OceanB.blend")
parser.add_argument('--output_path', help="Path to output directory.", default="outputs")
parser.add_argument('--haven_dir', help="Path to Haven directory.", default="resources/Haven")
parser.add_argument('--boat_dir', help="Path to boat directory.", default="resources/boats")
parser.add_argument('--mountain_dir', help="Path to mountain directory.", default="resources/mountains")
parser.add_argument('--buoy_dir', help="Path to buoy directory.", default="resources/buoys")
parser.add_argument('--starting_output', help="Number of the starting output.", default=0)
parser.add_argument('--number_of_outputs', help="Number of total outputs.", default=1)
args = parser.parse_args()

# Args: <config_file> <output_dir> <blend_file> <cam_file> <boat_dir> <mountain_dir> <buoy_dir> <haven_dir>

for i in range(args.number_of_outputs):
    output = 'Output' + str(int(args.starting_output)+i)
    os.system(f'cmd /c run.py {args.config_file} {args.output_path}/{output} {args.blend_file} {args.cam_file} {args.boat_dir} {args.mountain_dir} {args.buoy_dir} {args.haven_dir}')
