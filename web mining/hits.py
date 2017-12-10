
def normalize(dictionary):
    """ Normalize the values of a dictionary to sum up to 1. """
    norm = sum((dictionary[p] for p in dictionary))
    return {k: v / norm for (k, v) in dictionary.items()}

import operator
filename = 'web-Stanford.txt'
isDirected = True
from utils import parse
graph = parse(filename, isDirected)
node_count = len(graph)
damping_factor = 0.85


def calculate_scores(hub_score, auth_score):
    next_auth = dict()
    next_hub = dict()
    for key, node in graph.nodes(data=True):
        next_hub[key] = 0.0
    for key, node in graph.nodes(data=True):

        # compute auth score
        auth_sum = 0.0
        in_neighbors = graph.in_edges(key)
        for n in in_neighbors:
            auth_sum += hub_score[n[1]]
        next_auth[key] = auth_sum

        # compute hub score
        out_neighbors = graph.out_edges(key)
        for n in out_neighbors:
            next_hub[n[1]] += auth_score[key]

    next_auth = normalize(next_auth)
    next_hub = normalize(next_hub)

    return next_hub, next_auth


def get_hits_score():

    hub_score = dict()
    auth_score = dict()
    for key, node in graph.nodes(data=True):
        # ranks[key] = 1 / float(node_count)
        auth_score[key] = hub_score[key] = 1 / float(node_count)

    # perform 10 iterations
    for _ in range(10):
        hub_score, auth_score = calculate_scores(hub_score, auth_score)
    return hub_score, auth_score


hub_score, auth_score = get_hits_score()

sorted_r = sorted(hub_score.iteritems(), key=operator.itemgetter(1), reverse=True)
count = 0
print '{0:30} {1:10}'.format('Node ID', 'Hub Score')
for tup in sorted_r:
    print '{0:30} :{1:10}'.format(str(tup[0]), tup[1])
    count += 1
    if count == 10:
        break
