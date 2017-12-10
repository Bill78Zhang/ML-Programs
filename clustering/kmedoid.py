"""
 Created by Omkar Jadhav
"""

# The only difference between k-means and k-medoid algorithm is how we update
# centroid of cluster, in k-means it is just the mean of respective attribute
# values while in k-medoid it is actual point within the given cluster which
# is approximately at the center.


import numpy as np
import math
import random


# load data in np array format
def load_data():
    f = open('iris.data.txt', 'r')
    class_dict = {'Iris-versicolor': 0, 'Iris-setosa': 1, 'Iris-virginica': 2}
    dataset = []
    for s in f.readlines():
        s_list = s.split(',')[0:len(s)]
        tmp = list(map(float, s_list[:len(s_list) - 1]))
        tmp.append(int(class_dict[s_list[len(s_list) - 1].strip()]))
        dataset.append(tmp)

    return np.array(dataset, dtype=float)


def normalize_data(data):
    """
    Normalizes each column of data.
    :param data:
    :return:
    """
    attr_count = data.shape[1] - 1
    mean = np.mean(data[:, :-1], axis=0)
    std_dev = np.std(data[:, :-1], axis=0)
    for j in xrange(attr_count):
        data[:,j] = (data[:, j] - mean[j]) / std_dev[j]
    return data


def euclidean_dist(a, b):
    """
    Returns euclidean distance between two data points
    :param a: Data point as np array
    :param b: Data point B as np array
    :return: Returns distance between in float format
    """
    return math.sqrt(np.sum((a - b) ** 2))


def kmedoid_clustering(data, k=1, itrs=1000):
    """
    Implementation of kmeans clustering algorithm
    :param data:
    :param k: Number of clusters
    :param itrs: Max number of iterations to be performed
    :return: Clusters and points in them
    """

    attr_count = data.shape[1] - 1

    # create k random cluster centroids
    centroids = [[random.random() for __ in xrange(attr_count)] for _ in xrange(k)]
    clusters = [[] for _ in xrange(k)]
    print centroids
    for d in data:
        min_index = 0
        min_dist = euclidean_dist(d[:-1], centroids[0])
        for c_index in xrange(1, k):
            dist = euclidean_dist(d[:-1], centroids[c_index])
            if dist < min_dist:
                min_dist = dist
                min_index = c_index
        clusters[min_index].append(d)

    count = 0
    converged = False

    while count < itrs:
        converged = True
        tmp_clusters = [[] for _ in xrange(k)]
        for i in xrange(k):
            for d in clusters[i]:
                min_index = 0
                min_dist = euclidean_dist(d[:-1], centroids[0])
                for c_index in xrange(1, k):
                    dist = euclidean_dist(d[:-1], centroids[c_index])
                    if dist < min_dist:
                        min_dist = dist
                        min_index = c_index

                if min_index != i:
                    converged = False  # cause data point just switched its cluster
                tmp_clusters[min_index].append(d)

        for i in xrange(k):
            clusters[i] = tmp_clusters[i]
            centroids[i] = np.array([0]*attr_count , dtype=float)
            for d in clusters[i]:
                centroids[i] += d[:-1]

            centroids[i] /= len(clusters[i])

            # find point within cluster which is near to actual centroid
            min_dist = euclidean_dist(centroids[i], clusters[i][0][:-1])
            cen = clusters[0][:-1]
            for d in clusters[i]:

                dist = euclidean_dist(centroids[i], d[:-1])
                if dist < min_dist:
                    cen = d[:-1]
                    min_dist = dist
            # update medoid
            centroids[i] = cen

        count += 1

    return clusters


if __name__ == '__main__':
    id = 1
    k = 3  # number of clusters
    data = load_data()
    data = normalize_data(data)
    for cluster in kmedoid_clustering(data, k=3):
        cnt = [0] * 3
        for point in cluster:
            cnt[int(point[-1])] += 1
        print 'Cluster ', id, ' : ', cnt
        id += 1

