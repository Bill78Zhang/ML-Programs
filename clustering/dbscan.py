"""
 Created by Omkar Jadhav
"""

import numpy as np
import math

NOISE = -1
UNCLASSIFIED = 0
CLASSIFIED = 1


class DataPoint:
    def __init__(self, data, index, type=UNCLASSIFIED, cluster_index=-1):
        self.data = data
        self.index = index
        self.type = UNCLASSIFIED
        self.cluster_index = cluster_index


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


def euclidean_dist(a, b):
    """
    Returns euclidean distance between two data points
    :param a: Data point as np array
    :param b: Data point B as np array
    :return: Returns distance between in float format
    """
    return math.sqrt(np.sum((a - b) ** 2))


def get_neighbours(index, points, eps):
    neighbours = []
    core = points[index]
    for i in xrange(points.shape[0]):
        if i == index or points[i].type == CLASSIFIED:
            continue

        dist = euclidean_dist(core.data[:-1], points[i].data[:-1])
        if dist <= eps:
            neighbours.append(points[i])

    return neighbours


def db_scan(data, minpts=1, eps=0.0):

    # initialize all the data points as UNCLASSIFIED
    current_cluster = 1
    points = []
    row_count = data.shape[0]

    for i in xrange(row_count):
        points.append(DataPoint(data[i], i))

    points = np.array(points)

    for i in xrange(row_count):
        if points[i].type == UNCLASSIFIED:
            # if given point is still UNCLASSIFIED
            # check if it has got enough neighbours
            seeds = get_neighbours(i, points, eps)
            # check if given point is noise
            if len(seeds) + 1 < minpts:
                points[i].type = NOISE
                continue
        else:
            continue

        # to avoid repetitive processing of points
        considered = {i}
        for seed in seeds:
            considered.add(seed.index)

        core = points[i]
        core.type = CLASSIFIED
        core.cluster_index = current_cluster

        # expand cluster considering neighbours as seed points
        j = 0
        # first point analyzed will be core point
        while j < len(seeds):
            if seeds[j].type in [UNCLASSIFIED, NOISE]:
                if seeds[j].type == UNCLASSIFIED:

                    seeds[j].type = CLASSIFIED
                    seeds[j].cluster_index = current_cluster

                    new_neighbours = get_neighbours(seeds[j].index, points, eps)
                    # taking
                    for neighbour in new_neighbours:
                        if neighbour.type == UNCLASSIFIED and \
                                not considered.__contains__(neighbour.index):
                            seeds.append(neighbour)
                            considered.add(neighbour.index)

                else:
                    # then it must be a NOISE so we'll just keep it that way
                    # Reason: when a noise point is encountered it is possible that it is a
                    # boundary point and it may become part of two clusters at the same time,
                    # even we humans can't resolve this issue so we'll think of it as part
                    # of both clusters and it will contribute to min_pts criteria.
                     pass
            j += 1

        current_cluster += 1

    clusters = [0 for j in xrange(current_cluster)]
    noise_count = 0
    for point in points:
        if point.type != NOISE:
            clusters[point.cluster_index] += 1
        else:
            noise_count += 1

    for index in xrange(1, len(clusters)):
        print 'Cluster :', index, ' =>', clusters[index]

    print 'Noise:', noise_count
    return []


if __name__ == '__main__':

    data = normalize_data(load_data())
    np.random.shuffle(data)
    clusters = db_scan(data, 10, 0.50)