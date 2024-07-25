import numpy as np
import matplotlib.pyplot as plt
import os

class clip:
    def __init__(self, path:str):
        self.path = path
        self.x_lines, self.y_lines, self.matrix = self.Preprocess()
        self.str1 = self.turn_string(self.matrix)
        self.str2 = self.turn_string(np.transpose(self.matrix))
        self.str3 = self.turn_string(self.matrix[::-1])
        self.str4 = self.turn_string(np.transpose(self.matrix)[::-1])

    def Preprocess(self):
        x_lines = []
        y_lines = []
        lines = []
        with open(self.path, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("RECT"):
                    line = line.removeprefix("RECT N M1 ").split()
                    x_lines.append(int(line[0]))
                    x_lines.append(int(line[0]) + int(line[2]))
                    y_lines.append(int(line[1]))
                    y_lines.append(int(line[1]) + int(line[3]))
                    lines.append([int(line[0]),int(line[1]),int(line[1]) + int(line[3])])
                    lines.append([int(line[0]) + int(line[2]), int(line[1]), int(line[1]) + int(line[3])])

                elif line.startswith("PGON"):
                    line = line.removeprefix("PGON N M1 ").split()
                    for i in range(0,len(line),2):
                        if line[i] == line[(i + 2) % len(line)]:
                            x_lines.append(int(line[i]))
                            lines.append([int(line[i]),
                                          min(int(line[i + 1]),int(line[(i + 3) % len(line)])),
                                          max(int(line[i + 1]),int(line[(i + 3) % len(line)]))])
                        if line[i + 1] == line[(i + 3) % len(line)]:
                            y_lines.append(int(line[i + 1]))

        x_lines = list(set(x_lines))
        x_lines.append(2048)
        x_lines.sort()
        y_lines = list(set(y_lines))
        y_lines.append(0)
        y_lines.append(2048)
        y_lines.sort()
        image = np.zeros((len(y_lines) - 1,len(x_lines)))
        for i in range(len(y_lines) - 1):
            start = 0
            for j in range(len(x_lines)):
                image[i][j] = start
                in_ = False
                for x in lines:
                    if (x[0] == x_lines[j]) and (x[1] <= y_lines[len(y_lines) - i - 2]) and (x[2] >= y_lines[len(y_lines) - i - 1]):
                        in_ = True
                        break
                if in_ == True:
                    start = 1 if start == 0 else 0

        return x_lines[0:-1], y_lines[1:-1],image

    def turn_string(self,matrix):
        str = []
        for i in range(matrix.shape[1]):
            now = matrix[0][i]
            exp = 0
            num = 0
            num = num + now * (2**exp)
            for j in range(matrix.shape[0]):
                if matrix[j][i] == now:
                    continue
                else:
                    now = matrix[j][i]
                    exp += 1
                    num += now * (2**exp)
            str.append(num)
        return str


dict = "glp"
files = os.listdir(dict)
files = files[0:1000]

image_num = len(files)
cluster_num = 0

clusters = {}
st = 0
for file in files:
    print(st)
    st+=1

    c = clip('glp/' + file)
    c_str = c.str1 + c.str2
    c_strr = c.str1 + c.str2 + c.str3 + c.str4 + c.str1
    match = False
    for center in clusters.keys():
        c1 = clip('glp/' + clusters[center][0])
        c1_str = c1.str1 + c1.str2
        c1_strr = c1.str1 + c1.str2 + c1.str3 + c1.str4 + c1.str1
        if any(c_str == c1_strr[i:i+len(c_str)] for i in range(len(c1_strr) - len(c_str) + 1)) or\
            any(c1_str == c_strr[i:i + len(c1_str)] for i in range(len(c_strr) - len(c1_str) + 1)):
            clusters[center].append(file)
            match = True
            break
    print(match)
    if match == False:
        new_center = cluster_num
        cluster_num += 1
        clusters[new_center] = [file]
print(len(clusters.keys()))
for i in clusters.values():
    print(i)
    print(len(i))









