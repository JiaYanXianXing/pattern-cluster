import matplotlib.pyplot as plt
import numpy as np
import random
import math


class Sample_GONZALEZ:
    def __init__(self, data, k, n, e):
        self.data = data
        self.k = k
        self.n = n
        self.e = e
        self.centers = self.run()
        self.index = self.partition()

    def randCent(self):
        random_index = random.randint(0, self.data.shape[0] - 1)
        return random_index


    def sampling(self):
        sample = []
        for i in range(round(self.k / self.e * math.log(self.k / self.n, 2))):
            x = random.randint(0, self.data.shape[0] - 1)
            sample.append(x)
        return sample

    def distance_point(self, imageA, imageB):
        imageB_1 = np.rot90(imageB,1)
        imageB_2 = np.rot90(imageB, 2)
        imageB_3 = np.rot90(imageB, 3)


        imageB_4 = np.transpose(imageB)
        imageB_5 = np.rot90(imageB_4,1)
        imageB_6 = np.rot90(imageB_4, 2)
        imageB_7 = np.rot90(imageB_4, 3)

        xor = np.logical_xor(imageA,imageB) + 0
        xor1 = np.logical_xor(imageA,imageB_1) + 0
        xor2 = np.logical_xor(imageA, imageB_2) + 0
        xor3 = np.logical_xor(imageA, imageB_3) + 0
        xor4 = np.logical_xor(imageA, imageB_4) + 0
        xor5 = np.logical_xor(imageA, imageB_5) + 0
        xor6 = np.logical_xor(imageA, imageB_6) + 0
        xor7 = np.logical_xor(imageA, imageB_7) + 0

        return min(np.sum(xor),np.sum(xor1),np.sum(xor2),np.sum(xor3),\
                   np.sum(xor4),np.sum(xor5),np.sum(xor6),np.sum(xor7)) / (200 * 200)

    def distance_set(self, set, image):
        distance = self.distance_point(image,set[0])
        for i in range(len(set)):
            if self.distance_point(image,set[i]) == 0 :
                return 0
            if self.distance_point(image,set[i]) < distance:
                distance = self.distance_point(image,set[i])
        return distance

    def run(self):
        centers = []
        centers_index = []
        centers_index.append(self.randCent())
        centers.append(self.data[centers_index[0]])

        while len(centers) < self.k:
            print(len(centers))
            Q = self.sampling()
            max_distance = 0
            for index in Q:
                if self.distance_set(centers,self.data[index]) > max_distance:
                    max_distance = self.distance_set(centers,self.data[index])
                    max_index = index

            centers_index.append(max_index)
            centers.append(self.data[max_index])

        return centers

    def partition(self):
        index = [0] * self.data.shape[0]
        for i in range(self.data.shape[0]):
            distance = 1
            for j in range(len(self.centers)):
                if self.distance_point(self.data[i],self.centers[j]) < distance:
                    distance = self.distance_point(self.data[i],self.centers[j])
                    index[i] = j
        return index


#测试数据为2.npy
data = np.load('2.npy')
k = 20
model = Sample_GONZALEZ(data,k,0.5,0.5)
s = [0] * k
print(model.index)
for i in range(len(model.index)):
    plt.imsave('out1/'+str(model.index[i])+'.'+str(s[model.index[i]])+'.png', data[i])
    s[model.index[i]] = s[model.index[i]] +1
print(s)
#计算kcenter的最大半径
max_d = 0
for i in range(data.shape[0]):
    d = model.distance_point(data[i],model.centers[model.index[i]])
    if d >max_d:
        max_d = d
print(max_d)