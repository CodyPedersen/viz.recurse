"""Example usage for the visualization library"""
import json

from vizrecurse import draw, visualize, graph_repr


@visualize
def toh(n, source, destination, auxiliary):
    """Visualization demo for towers of hanoi"""
    if n==1:
        print ("Move disk 1 from source", source, "to destination", destination)
        return
    toh(n-1, source, auxiliary, destination)
    print ("Move disk", n,"from source", source, "to destination", destination)
    toh(n-1, auxiliary, destination, source)


@visualize
def linear_recurse(n):
    """Visualization demo for simple recursion"""
    if n <= 0:
        return
    print(n)
    linear_recurse(n-1)


# Driver code
N = 5
toh(N,'A','B','C')
#linear_recurse(N)

graph = graph_repr()

with open('./graph.json', 'w') as f:
    json.dump(graph, f)

draw()
