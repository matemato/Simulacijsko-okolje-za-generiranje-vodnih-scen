import os

path = "../images"

os.chdir(path)

f = open("train.txt", "a")

for i, pic in enumerate(os.listdir()):
    f.write(pic)
    f.write(' ')
    if i%2==1:
        f.write('imu.png\n')

f.close()