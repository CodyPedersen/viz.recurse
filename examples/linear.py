# pylint: disable=wrong-import-position, import-error
"""Example: Linear regression visualization. Runnable as script."""
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
def linear_recurse(n: int) -> None:
    """Visualization demo for simple recursion"""
    if n <= 0:
        return
    print(n)
    linear_recurse(n-1)

linear_recurse(5)

graph = graph_repr()
print(graph)
dump_graph(fileloc="linear-recurse.json")
draw()
