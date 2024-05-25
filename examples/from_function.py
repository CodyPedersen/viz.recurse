# pylint: disable=wrong-import-position, import-error
"""Example usage for the visualization library from a function. Runnable as script."""
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
def fib(n: int) -> int:
    """Return nth fibonacci number"""
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

def my_fn() -> int:
    """my fn"""
    return fib(5)

my_fn()

graph = graph_repr()
print(graph)
dump_graph(fileloc="fib.json")
draw(node_size=600, font_size=6)
