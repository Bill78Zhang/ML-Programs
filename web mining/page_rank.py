import operator
from utils import parse

filename = 'web-Stanford.txt'
isDirected = True
graph = parse(filename, isDirected)
node_count = len(graph)
damping_factor = 0.85
ranks = dict()


def get_ranks():
    for key, node in graph.nodes(data=True):
        ranks[key] = 1 / float(node_count)

    for _ in range(2):
        for key, node in graph.nodes(data=True):
            rank_sum = 0
            neighbors = graph.in_edges(key)
            for n in neighbors:
                outlinks = len(graph.out_edges(n[1]))
                if outlinks > 0:
                    rank_sum += (1 / float(outlinks)) * ranks[n[1]]

            ranks[key] = damping_factor * rank_sum + ((1 - float(damping_factor)) * (1 / float(node_count)))

get_ranks()
sorted_r = sorted(ranks.iteritems(), key=operator.itemgetter(1), reverse=True)
count = 0
print '{0:30} {1:10}'.format('Node ID', 'Page rank')
for tup in sorted_r:
    count += 1
    print '{0:30} :{1:10}'.format(str(tup[0]), tup[1])
    if count == 10:
        break
