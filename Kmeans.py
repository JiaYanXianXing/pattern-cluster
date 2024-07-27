import numpy as np
import time

class KMeans:
    def __init__(self, K, data):
        self.K = K
        self.data = data
        self.centroids = None
        self.clusters = {i: [] for i in range(K)}

    def initialize_centroids(self):
        # 随机选择K个数据点作为初始质心
        indices = np.random.choice(len(self.data), self.K, replace=False)
        self.centroids = self.data[indices]

    def assign_clusters(self):
        # 将每个数据点分配到最近的质心
        clusters = {i: [] for i in range(K)}
        for i, point in enumerate(self.data):
            distances = [self.distance_point(point, centroid) for centroid in self.centroids]
            closest_centroid = np.argmin(distances)
            clusters[closest_centroid].append(i)
        self.clusters = clusters

    def update_centroids(self):
        # 根据簇内所有点的均值更新质心
        for cluster_id, indices in self.clusters.items():
            if indices:  # 确保簇不为空
                self.centroids[cluster_id] = np.mean(self.data[indices], axis=0)

    def distance_point(self, imageA, imageB):
        imageB_1 = np.rot90(imageB, 1)
        imageB_2 = np.rot90(imageB, 2)
        imageB_3 = np.rot90(imageB, 3)

        imageB_4 = np.transpose(imageB)
        imageB_5 = np.rot90(imageB_4, 1)
        imageB_6 = np.rot90(imageB_4, 2)
        imageB_7 = np.rot90(imageB_4, 3)

        xor = np.logical_xor(imageA, imageB) + 0
        xor1 = np.logical_xor(imageA, imageB_1) + 0
        xor2 = np.logical_xor(imageA, imageB_2) + 0
        xor3 = np.logical_xor(imageA, imageB_3) + 0
        xor4 = np.logical_xor(imageA, imageB_4) + 0
        xor5 = np.logical_xor(imageA, imageB_5) + 0
        xor6 = np.logical_xor(imageA, imageB_6) + 0
        xor7 = np.logical_xor(imageA, imageB_7) + 0

        return min(np.sum(xor), np.sum(xor1), np.sum(xor2), np.sum(xor3), \
                   np.sum(xor4), np.sum(xor5), np.sum(xor6), np.sum(xor7)) / (200 * 200)

    def fit(self, max_iterations=100):
        start_time = time.time()
        self.initialize_centroids()
        for iteration in range(max_iterations):
            self.assign_clusters()
            print(self.clusters)
            previous_centroids = np.copy(self.centroids)
            self.update_centroids()
            if np.allclose(previous_centroids, self.centroids):
                break
        end_time = time.time()
        print(f"KMeans clustering took {end_time - start_time:.2f} seconds.")

    def predict(self, new_data):
        # 预测新数据点的簇分配
        distances = [self.distance_point(new_data, centroid) for centroid in self.centroids]
        return np.argmin(distances)

    def count_clusters(self):
        # 统计每个簇包含的数据点数目
        return {i: len(self.clusters[i]) for i in range(self.K)}

    def calculate_max_radii(self):
        # 计算每个簇的最大半径
        max_radii = {}
        for i in range(self.K):
            distances = [self.distance_point(self.data[idx], self.centroids[i]) for idx in self.clusters[i]]
            max_radius = max(distances) if distances else 0
            max_radii[i] = max_radius
        return max_radii

# 使用示例
# 假设data是一个包含若干200x200二值图像的NumPy数组
# K是簇的数量
K = 5
data = np.load('1.npy')
kmeans = KMeans(K, data)
kmeans.fit()
print(kmeans.clusters)
# 统计每个簇的数据点数目
cluster_counts = kmeans.count_clusters()
print("Cluster counts:", cluster_counts)

# 计算每个簇的最大半径
cluster_radii = kmeans.calculate_max_radii()
print("Cluster radii:", cluster_radii)
