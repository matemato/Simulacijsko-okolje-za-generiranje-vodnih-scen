import os
from shutil import copyfile

path = "../outputs"
imgPath = "../../images"

# os.chdir(path)
start = 0

for output in os.listdir(path):
    if len(output) == 7:
        name = output[:6] + '00' + output[6:]
        os.rename(output, name)
    elif len(output) == 8:
        name = output[:6] + '0' + output[6:]
        os.rename(output, name)
        
for i,output in enumerate(os.listdir(path)):
    if (len(output) == 9 and int(output[6:9]) >= start) or (len(output) == 10 and int(output[6:10]) >= start):
        os.chdir(path + '/' + output)
        for img in os.listdir(os.getcwd()):
            if len(os.listdir(os.getcwd())) > 1:
                print(os.getcwd())
                if 'rgb' in img:
                    copyfile(img, imgPath + '/' + output + 'image.png')
                else:
                    copyfile(img, imgPath + '/' + output + 'segmap.png')
