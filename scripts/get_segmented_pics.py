import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
from pycocotools.coco import COCO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--object_type', help="Which object to segment.", default="boat")
parser.add_argument('--annotation_type', nargs='+', help="Which annotation type.", default=["lvis_val"], choices=["lvis_val", "lvis_train" "coco_val", "coco_train"])
args = parser.parse_args()

output_path = f'../resources/{args.object_type}s'

if not os.path.exists(output_path):
    os.mkdir(output_path)

n = 0

object_name = args.object_type

for data in args.annotation_type:
    print(data)
    annFile=f'../resources/annotations/{data}.json'
    coco=COCO(annFile)

    catIds = coco.getCatIds(catNms=args.object_type)  
    imgIds = coco.getImgIds(catIds=catIds)
    print(len(imgIds))
    for id in imgIds:
        img = coco.loadImgs(id)[0]
        annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
        anns = coco.loadAnns(annIds)
        html = img['coco_url']
        img_name = html.split('/')[4]
        print(img_name)
        I = cv2.imread(f'../resources/COCO_val/' + img_name)
        if I is None:
            I = cv2.imread(f'../resources/COCO_train/' + img_name)      
        I = cv2.cvtColor(I, cv2.COLOR_RGB2RGBA)
        for ann in anns:
            name = object_name+str(n)
            imgPath = os.path.join(output_path, name) +'.png'

            x = int(ann['bbox'][0])
            y = int(ann['bbox'][1])
            w = int(ann['bbox'][2])
            h = int(ann['bbox'][3])

            if w > 10 and h > 10:
                mask = coco.annToMask(ann)
                mask[mask==1] = 255
                alpha = cv2.GaussianBlur(mask,(5,5),1,borderType=cv2.BORDER_CONSTANT)
                I[:, :, 3] = alpha
                cropped = I[y:y+h, x:x+w]
                cv2.imwrite(imgPath,cropped)  
                n += 1
                
print("Finished")
