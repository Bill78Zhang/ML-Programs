
import numpy as np
import heapq
import math


def load_data():
    x = []
    train_y = []
    f = open('Iris/train.data', 'r')
    class_map = {'Iris-versicolor': 1, 'Iris-setosa': 2, 'Iris-virginica': 3}
    for s in f.readlines():
        s_list = s.split(',')
        x.append(map(float, s_list[:len(s_list) - 1]))  # split input and output and create arrays
        train_y.append(float(class_map[s_list[-1].strip()]))
    train_x = np.array(x, dtype=float)
    train_y = np.array(train_y, dtype=float)

    x = []
    test_y = []
    f = open('Iris/test.data', 'r')
    for s in f.readlines():
        s_list = s.split(',')[0:len(s)]
        x.append(map(float, s_list[:len(s_list) - 1]))  # split input and output and create arrays
        test_y.append(float(class_map[s_list[len(s_list) - 1].strip()]))
    x_test = np.array(x, dtype=float)
    test_y = np.array(test_y, dtype=float)
    return train_x, train_y, x_test, test_y

c = 3  # number of classes
n = 5  # number of parameters


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0
        self._count = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1
        self._count += 1

    def pop(self):
        self._count -= 1
        return heapq.heappop(self._queue)[-1]

    def queue_size(self):
        return self._count

    def is_empty(self):
        return self._count == 0


def euclidean_distance(point_a, point_b):
    return math.sqrt(np.sum((point_a.attribute_values - point_b.attribute_values) ** 2))


class DataPoint:
    def __init__(self, values, my_class=-1):
        self.attribute_values = values
        self.my_class = my_class


def knn_classify(x_train, y_train, x_test, n_neighbours=5):
    count = yg_test.size
    train_count = y_train.size
    result = np.array([0]*count)
    for i in xrange( count ):
        q = PriorityQueue()
        test_point = DataPoint(x_test[i])
        for j in xrange(train_count):
            train_point = DataPoint(x_train[j], y_train[j])
            dist1 = euclidean_distance(train_point, test_point)

            if q.queue_size() < n_neighbours :
                q.push(train_point, dist1)
            else:
                queue_top = q.pop()
                dist2 = euclidean_distance(queue_top, test_point)
                if dist1 < dist2:
                    q.push(train_point, dist1)
                else:
                    q.push(queue_top, dist2)

        class_count = [0] *(c + 1)
        while not q.is_empty():
            top = q.pop()
            class_count[int(top.my_class)] += 1

        # print class_count

        for j in xrange(1, c + 1):
            if class_count[j] == max(class_count):
                result[i] = j
                break
    return result


xg_train, yg_train, xg_test, yg_test = load_data()

predicted = knn_classify(xg_train, yg_train, xg_test, 6)
count = 0
for _ in range(predicted.size):
    print 'Expected :', yg_test[_], '  Predicted:', predicted[_]
    if yg_test[_] == predicted[_]:
        count += 1
print('Accuracy is ', count / (float)(predicted.size))