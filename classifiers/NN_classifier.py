from math import exp
from random import seed
from random import random

# get data into np arrays
def create_data():
    train_dataset = []
    test_dataset = []
    f = open('Iris/train.data', 'r')
    dict = {'Iris-versicolor' : 0, 'Iris-setosa': 1, 'Iris-virginica': 2}
    for s in f.readlines():
        s_list = s.split(',')[0:len(s)]
        tmp = list(map(float, s_list[:len(s_list)-1]))
        tmp.append(int(dict[s_list[len(s_list) - 1].strip()]))
        train_dataset.append(tmp)

    f = open('Iris/test.data', 'r')
    for s in f.readlines():
        s_list = s.split(',')[0:len(s)]
        tmp = list(map(float, s_list[:len(s_list)-1]))
        tmp.append(int(dict[s_list[len(s_list) - 1].strip()]))
        test_dataset.append(tmp)

    return train_dataset,test_dataset


# test

# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list()
    hidden_layer = [{'weights':[random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights':[random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
    network.append(output_layer)
    return network


# Calculate neuron activation for an input
def activate(weights, inputs):
    activation = weights[-1] # add bias
    for i in range(len(weights)-1):
        activation += weights[i] * inputs[i]
    return activation


# Transfer neuron activation
def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))


# Forward propagate input to a network output
def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs


# Calculate the derivative of an neuron output
def transfer_derivative(output):
    return output * (1.0 - output)


# Backpropagate error and store in neurons
def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network)-1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])


# Update network weights with error
def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            # update weights
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
            # update bias
            neuron['weights'][-1] += l_rate * neuron['delta']


# Train a network for a fixed number of epochs
def train_network(network, train, l_rate, n_iterations, n_outputs):
    for i in range(n_iterations):
        sum_error = 0
        for row in train:
            outputs = forward_propagate(network, row)
            expected = [0] * n_outputs
            expected[row[-1]] = 1
            sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)
        #print('>epoch=%damping_factor, lrate=%.3f, error=%.3f' % (i, l_rate, sum_error))


# Make a prediction with a network
def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))


# Test training backprop algorithm
seed(1)
train_dataset, test_dataset = create_data()
n_inputs = 4
n_outputs = 3
#print(train_dataset)
network = initialize_network(n_inputs, 2, n_outputs)
train_network(network, train_dataset, 0.25, 200, n_outputs)
for layer in network:
    print(layer)

score=0
for row in test_dataset:
    prediction = predict(network, row)
    if row[-1] == prediction :
            score = score+1
    print('Expected: %d  Predicted: %d' % (row[-1] + 1, prediction + 1))

print 'Testing dataset size : ',len(test_dataset),' correct : ',score,' incorrect : ',(len(test_dataset)-score)
print 'Accuracy is ',100*score/len(test_dataset), '%'
