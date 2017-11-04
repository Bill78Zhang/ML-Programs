"""
   Created by Omkar Jadhav.
"""

import numpy as np
import math
import copy


class Cluster:
    def __init__(self, index, points, cluster_1=None, cluster_2=None):

        if points is None:
            self.index = index
            self.points = copy.copy(cluster_1.points)
            for other in cluster_2.points:
                self.points = np.vstack([self.points, other])

        else:
            self.index = index
            self.points = np.array([points])



class Pair:
    """
        Represents pair of cluster which will eventually stored
        in heap along with distance between them.
    """

    def __init__(self, cluster_1, cluster_2):
        self.cluster = []
        self.cluster.append(cluster_1)
        self.cluster.append(cluster_2)
        self.priority = find_priority(cluster_2, cluster_1)

    def __cmp__(self, other):
        return self.priority < other.priority


def euclidean_dist(a, b):
    """
    Returns euclidean distance between two data points
    :param a: Data point as np array
    :param b: Data point B as np array
    :return: Returns distance between in float format
    """
    return math.sqrt(np.sum((a - b) ** 2))


def find_priority(cluster_1, cluster_2):
    """
        Finds average of euclidean distances between each pair of cluster1 and cluster2
    :param cluster_1:
    :param cluster_2:
    :return:
    """
    distance_sum = 0.0
    for a in cluster_1.points:
        for b in cluster_2.points:
            distance_sum += euclidean_dist(a[:-1], b[:-1])
    N = len(cluster_2.points)
    M = len(cluster_1.points)

    return distance_sum / (N * M)


def hierarchical_clustering(data, cluster_count=1, ):
    clusters = []  # vector of clusters
    size = data.shape[0]
    cluster_index = 0
    for i in xrange(size):
        #print data[i]
        clusters.append(Cluster(cluster_index, data[i]))
        cluster_index += 1

    # originally we need to check whether this clusters are having enough distance between them
    # but for Iris data set we know that we're going to have 3 clusters so I chose below termination
    # condition(which is actually not part of algorithm)

    while len(clusters) > cluster_count:
        pairs = []
        size = len(clusters)
        for i in xrange(size):
            for j in xrange(i + 1, size):
                pairs.append(Pair(clusters[i], clusters[j]))
        min_dist = pairs[0].priority  # just random max value
        c_index = [0]*2
        for j in xrange(0, len(pairs)):
            if min_dist >= pairs[j].priority:
                min_dist = pairs[j].priority
                for i in xrange(2):
                    c_index[i] = pairs[j].cluster[i].index

        tmp_clu = []
        merged = []
        for cluster in clusters:
            if cluster.index == c_index[0] or cluster.index == c_index[1]:
                merged.append(cluster)
                continue
            tmp_clu.append(cluster)

        cluster_index += 1
        new_cluster = Cluster(cluster_index,None, merged[0], merged[1])
        tmp_clu.append(new_cluster)
        clusters = copy.copy(tmp_clu)

    return clusters


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

if __name__ == '__main__':
    id = 1
    data = load_data()
    for cluster in hierarchical_clustering(data, cluster_count=3):
        cnt = [0] * 3
        for point in cluster.points:
            cnt[int(point[-1])  ] += 1
        print 'Cluster ', id, ' : ', cnt
        id += 1