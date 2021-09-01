import random

f = open("../images/train.txt", "r")
fi = open("../images/train2.txt", "w")
a = []
b = []
n = 0
GPUs = 2
synthetic = True
counter = 0

for i,x in enumerate(f):
	if "Output" in x or "animation" in x:
		a.append(x)
	else:
		b.append(x)
	n += 1
	
random.shuffle(a)
random.shuffle(b)

print(a[0])

for i in range(n):
	if synthetic:
		fi.write(a[0])
		print(a[0])
		a.pop(0)
	else:
		fi.write(b[0])
		print(b[0])
		b.pop(0)
	if i%GPUs == GPUs-1:
		if not synthetic:
			counter += 1
			if counter%4 == 0:
				synthetic = not synthetic
		else:
			counter +=1
			synthetic = not synthetic
		
f.close()
fi.close()

	
