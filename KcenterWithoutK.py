import matplotlib.pyplot as plt
import numpy as np
import random
import math


class Sample_GONZALEZ_No_K:
    def __init__(self, data, r0, k0, n, e):
        self.data = data
        self.r0 = r0
        self.k0 = k0
        self.n = n
        self.e = e
        self.centers = self.run()
        self.index = self.partition()

    def randCent(self):
        random_index = random.randint(0, self.data.shape[0] - 1)
        return random_index


    def sampling(self, n):
        sample = []
        for i in range(n):
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
        t = 0
        i = 0

        while(True):
            print('t=',t)
            n0 = self.n / ((2 ** (2*t)) * self.k0)
            S = self.sampling(round(12 /(n0 * self.e) * math.log(2 / n0)))
            not_cover = set()
            for index in S:
                target = False
                for c in centers:
                    if self.distance_point(self.data[index],c) < self.r0:
                        target = True
                        break
                if target == False:
                    not_cover.add(index)


            for j in range((2 ** t) * self.k0):
                print('j=',j)
                Q = self.sampling(round(2 ** (2*t) * 2 * self.k0 / self.e * math.log(2 ** (2*t) * self.k0) / self.n))
                max_distance = 0
                for index in Q:
                    if self.distance_set(centers, self.data[index]) > max_distance:
                        max_distance = self.distance_set(centers, self.data[index])
                        max_index = index

                centers_index.append(max_index)
                centers.append(self.data[max_index])

                delete = []

                for index in not_cover:
                    if self.distance_point(self.data[index], self.data[max_index]) < self.r0:
                        delete.append(index)

                for d in delete:
                    not_cover.remove(d)

                if len(not_cover) / len(S) <= (1.5 * self.e):
                    return centers

            t = t + 1


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
data = np.load('3.npy')
r0 = 0.1
k0 = 2
n = 0.1
e = 0.01
model = Sample_GONZALEZ_No_K(data,r0,k0,n,e)
cs = model.centers

s = [0] * len(cs)
print(model.index)
for i in range(len(model.index)):
    plt.imsave('out1/'+str(model.index[i])+'.'+str(s[model.index[i]])+'.png', data[i])
    s[model.index[i]] = s[model.index[i]] +1
print(s)
#计算kcenter的最大半径
cd = [0] * len(cs)
max_d = 0
for i in range(data.shape[0]):
    d = model.distance_point(data[i],model.centers[model.index[i]])
    if d >max_d:
        max_d = d
    if d > cd[model.index[i]]:
        cd[model.index[i]] = d
print(max_d)
print(cd)