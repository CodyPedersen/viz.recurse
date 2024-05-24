"""Recursion visualization toolkit"""
import inspect
import logging

import networkx as nx
import matplotlib.pyplot as plt

from networkx.drawing.nx_pydot import graphviz_layout

G = nx.DiGraph()


def __dump_frame_info(frame):
    logging.info('\n\n')
    logging.info(f"frame_addr: {hex(id(frame))}")
    logging.info(f"frame: {repr(frame)}")
    logging.info(f"frame.f_locals {frame.f_locals}", end='\n')
    logging.info(f"dir(frame) {dir(frame)}", end='\n')
    logging.info(f"frame.f_code.co_nam {frame.f_code.co_name}", end='\n')
    logging.info(f"inspect.getframeinfo(frame): {inspect.getframeinfo(frame)}")


def visualize(func):
    """Decorator for visualization of recursive calls"""

    def inner(*args, **kwargs):
        cur_frame = inspect.currentframe()
        prev_frame = cur_frame.f_back

        cur_addr = hex(id(cur_frame))
        G.add_node(cur_addr, label=func.__name__+str(args))

        # if not coming from main context, build edge
        if prev_frame.f_locals.get('__name__') != '__main__':
            prev_wrapped_frame = prev_frame.f_back

            # Construct arguments from previous stack frame
            prev_wrapped_addr = hex(id(prev_wrapped_frame))
            G.add_edge(prev_wrapped_addr, cur_addr)

        return func(*args, **kwargs)

    return inner

def draw(font_size=8, gv_layout="dot", arrow_size=7, node_size=70) -> None:
    """Draw recursive tree/list from captured graph"""
    pos = graphviz_layout(G, prog=gv_layout)
    labels = {node: data['label'] for node, data in G.nodes(data=True)}

    nx.draw_networkx_nodes(G, pos, node_size=node_size)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='-|>', arrowsize=arrow_size)
    nx.draw_networkx_labels(G, pos, font_size=font_size, font_family='sans-serif', labels=labels)

    #nx.draw(G, pos)
    plt.show()


def graph_repr() -> dict:
    """Returns a dict representation of the call graph"""

    labels = {node: data['label'] for node, data in G.nodes(data=True)}

    # Format nodes and edges to distinct variation
    nodes = [f"{k}.{v}" for k,v in labels.items()]
    edges = [
        (f"{src}.{labels[src]}", f"{dst}.{labels[dst]}")
        for src, dst in G.edges()
    ]

    return {
        "nodes": nodes,
        "edges": edges
    }



# Execution flow
#
#   """"""""
#   @visualize
#   def some_function(args, kwargs): ...
#   """"""""
#   <__name__ = __main__ context> <-- prev on call stack
#   This calls visualize(func)  # no impact
#   visualize(func) his returns inner(*args, **kwargs)
#   inner(*args, **kwargs) is executed <-- [snapshot] cur on call stack
#   this calls custom function `toh(*args)` <-- prev on call stack
#   toh() calls visualize(func)
#   this returns inner(*args, **kwargs)
#   inner(*args, **kwargs) is executed <-- [snapshot] cur on call stack
#
