"""FIXME: add docstring"""
import inspect
import logging

import networkx as nx
import matplotlib.pyplot as plt

from networkx.drawing.nx_pydot import graphviz_layout

G = nx.Graph()


def dump_frame_info(frame):
    logging.info('\n\n')
    logging.info(f"frame_addr: {hex(id(frame))}")
    logging.info(f"frame: {repr(frame)}")
    logging.info(f"frame.f_locals {frame.f_locals}", end='\n')
    logging.info(f"dir(frame) {dir(frame)}", end='\n')
    logging.info(f"frame.f_code.co_nam {frame.f_code.co_name}", end='\n')
    logging.info(f"inspect.getframeinfo(frame): {inspect.getframeinfo(frame)}")


def visualize(func):
    """FIXME: add docstring"""
    #calling_frame = inspect.currentframe()
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

def draw(font_size=9, gv_layout="dot") -> None:
    """Draw recursive tree/list from captured graph"""
    pos = graphviz_layout(G, prog=gv_layout)
    labels = {node: data['label'] for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, font_size=font_size, font_family='sans-serif', labels=labels)
    nx.draw(G, pos)
    plt.show()



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
