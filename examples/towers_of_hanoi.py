# pylint: disable=wrong-import-position, import-error
"""Example usage for the visualization library. Runnable as script."""
import os
import sys

sys.path.append(os.path.dirname('..'))

from vizrecurse import (
    draw,
    dump_graph,
    graph_repr,
    visualize
)


@visualize
def toh(n: int, source: str, destination: str, auxiliary: str) -> None:
    """Visualization demo for towers of hanoi"""
    if n==1:
        print ("Move disk 1 from source", source, "to destination", destination)
        return
    toh(n-1, source, auxiliary, destination)
    print ("Move disk", n,"from source", source, "to destination", destination)
    toh(n-1, auxiliary, destination, source)


toh(5,'A','B','C')

graph = graph_repr()
print(graph)
dump_graph(fileloc='towers_of_hanoi.json')
draw()
