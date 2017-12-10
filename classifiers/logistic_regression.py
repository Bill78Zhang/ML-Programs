
import numpy as np


def load_data():
    x = []
    y_train = []
    f = open('Iris/train.data', 'r')
    dict = {'Iris-versicolor': 1, 'Iris-setosa': 2, 'Iris-virginica': 3}
    for s in f.readlines():
        s_list = s.split(',')[0:len(s)]
        x.append(map(float, s_list[:len(s_list) - 1]))  # split input and output and create arrays
        y_train.append(float(dict[s_list[len(s_list) - 1].strip()]))
    x_train = np.array(x, dtype=float)
    y_train = np.array(y_train, dtype=float)

    x = []
    y_test = []
    f = open('Iris/test.data', 'r')
    for s in f.readlines():
        s_list = s.split(',')[0:len(s)]
        x.append(map(float, s_list[:len(s_list) - 1]))  # split input and output and create arrays
        y_test.append(float(dict[s_list[len(s_list) - 1].strip()]))
    x_test = np.array(x, dtype=float)
    y_test = np.array(y_test, dtype=float)
    return x_train, y_train, x_test, y_test

c = 3 # number of classes
n = 5 # number of parameters


def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))


def train(x, y, alpha, iterations=1000):
    m = y.size
    theta = np.array([0]*n)  # initial values of theta
    i = 0
    while i < iterations:
        updated = np.zeros(n)
        for j in range(n):
            sub = 1 / float(m) * np.sum((sigmoid(theta.T.dot(x.T).T) - y) * x[:, j])
            updated[j] = theta[j] - alpha * sub
        theta = updated
        i += 1
    return theta


xTrain, yTrain, xTest, yTest = load_data()
t_theta = np.array(np.c_[[[0] * n] * c], dtype=float)
xTrain = np.c_[np.ones(xTrain.shape[0]), xTrain]
xTest = np.c_[np.ones(xTest.shape[0]), xTest]


# print xTrain
for i in xrange(0, c):
    #  update Y for "one against others" strategy
    tmpY=np.copy(yTrain)

    for j in xrange(len(tmpY)):
        if tmpY[j] == i + 1:
            tmpY[j] = 1
        else:
            tmpY[j] = 0
    t_theta[i] = train(xTrain, tmpY, alpha=0.1)

print 'Values of theta...'
print t_theta
test_size = yTest.size


def predict(x, _theta):
    n_class = 3
    res_class = 0
    max_value = -2
    for i in xrange(n_class):
        theta_i = _theta[i]
        value = sigmoid(theta_i.T.dot(x))
        if value > max_value:
            max_value = value
            res_class = i + 1
    return res_class


for i in xrange(test_size):
    result = predict(xTest[i], t_theta)
    print 'Expected: ', yTest[i], ' Predicted:', result
