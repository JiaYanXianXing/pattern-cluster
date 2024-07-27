import matplotlib.pyplot as plt
import numpy as np
from KMP import kmp_search
import time
class clip:
    def __init__(self, image):
        self.image = image
        self.get_str()
        self.get_pattarn()
        self.str = self.str1 + self.str2

    # 裁剪图像，去除边界的0
    def remove_border_zeros(self,image):
        top_border = 0
        while top_border < 200 and image[top_border].sum() == 0:
            top_border += 1

        bottom_border = 200 - 1
        while bottom_border >= 0 and image[bottom_border].sum() == 0:
            bottom_border -= 1

        left_border = 0
        while left_border < 200 and (image[:, left_border].sum() == 0):
            left_border += 1

        right_border = 200 - 1
        while right_border >= 0 and (image[:, right_border].sum() == 0):
            right_border -= 1

        cropped_image = image[top_border:bottom_border + 1, left_border:right_border + 1]
        return cropped_image

    def find_lines(self,image):
        lines = []
        (x, y) = image.shape
        for i in range(y - 1):
            for j in range(x):
                if image[j][i] != image[j][i + 1]:
                    lines.append(i)
                    break
        if len(lines) > 0 :
            lines.append(lines[-1] + 1)
        else:
            lines.append(0)
        return lines

    def turn_str(self,lines,image):
        (x, y) = image.shape
        str = [0] * (len(lines))
        for (i, index) in enumerate(lines):
            str[i] = str[i] * 2 + 1
            elem = image[0][index]
            str[i] = str[i] * 2 + elem
            for j in range(1, x):
                if image[j][index] != elem:
                    elem = image[j][index]
                    str[i] = str[i] * 2 + elem
        return str

    def get_str(self):
        self.image = self.remove_border_zeros(self.image)
        (x, y) = self.image.shape

        lines = self.find_lines(self.image)
        self.str1 = self.turn_str(lines,self.image)
        self.str3 = self.turn_str(lines,np.flip(self.image,axis=0))

        rot90 = np.rot90(self.image,-1)
        lines_ = self.find_lines(rot90)
        self.str2 = self.turn_str(lines_,rot90)
        self.str4 = self.turn_str(lines_, np.flip(rot90, axis=0))

    def get_pattarn(self):
        self.str3.reverse()
        self.str4.reverse()
        self.pattarn0 = self.str1 + self.str2 + self.str3 + self.str4 + self.str1
        self.str3.reverse()
        self.str4.reverse()
        self.str1.reverse()
        self.str2.reverse()
        self.pattarn1 = self.str1 + self.str4 + self.str3 + self.str2 + self.str1
        self.str1.reverse()
        self.str2.reverse()

data = np.load('4.npy')

clusters = {}
cluster_num = 0

start_time = time.time()
creat_time = 0

for i,image in enumerate(data):
    print(i)
    cr_s = time.time()
    if image.sum() == 0:
        continue
    c = clip(image)
    cr_e = time.time()
    creat_time += cr_e - cr_s

    match = False
    for center in clusters.keys():

        c1 = clusters[center][0]

        if len(c.str) > len(c1.str):
            if kmp_search(c.pattarn0,c1.str) or kmp_search(c.pattarn1,c1.str):
                clusters[center].append(c)
                match = True
                break
        else:
            if kmp_search(c1.pattarn0,c.str) or kmp_search(c1.pattarn1,c.str):
                clusters[center].append(c)
                match = True
                break
    if match == False:
        new_center = cluster_num
        cluster_num += 1
        clusters[new_center] = [c]
end_time = time.time()
print('clusters num:',str(len(clusters.keys())))
print('total time:')
print(end_time -start_time)
print('creat time:')
print(creat_time)
print('cluster time')
print(end_time - start_time-creat_time)
for i in clusters.keys():
    for j in range(len(clusters[i])):
        plt.imsave('out1/'+str(i)+'.'+str(j)+'.png', clusters[i][j].image)






        

