f = open('Iris/iris.data.txt', 'r')
trainData = open('Iris/train.data', 'w')
testData = open('Iris/test.data', 'w')
lines = f.readlines()
dict = {}
for i in xrange(0, len(lines)):
    s = lines[i].split(',')[-1]
    if dict.get(s) is None:
        dict[s] = []
    dict.get(s).append(lines[i])

for s in dict.keys():
    data = dict[s]
    size = len(data)
    trainData.writelines(data[0:int(0.7*size)])
    testData.writelines(data[int(0.7*size):len(data)])

f.close()
testData.close()
trainData.close()
