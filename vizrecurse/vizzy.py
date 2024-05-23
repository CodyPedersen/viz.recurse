"""FIXME: add docstring"""
import inspect

from itertools import count

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
unique_id_counter = count(start=1)

def generate_execution_id():
    return next(unique_id_counter)


def visualize(func):
    """FIXME: add docstring"""
    #calling_frame = inspect.currentframe()
    def inner(*args, **kwargs):
        cur_frame = inspect.currentframe()
        prev_frame = cur_frame.f_back

        print('\n\n')
        print(hex(id(prev_frame)))
        print(f"repr(prev_frame): {repr(prev_frame)}")
        print(f"\n\nprev frame: {prev_frame}\n")
        print(f"prev_frame.f_locals {prev_frame.f_locals}", end='\n')
        print(f"dir(prev_fame) {dir(prev_frame)}", end='\n')
        print(f"prev_frame.f_code.co_nam {prev_frame.f_code.co_name}", end='\n')
        print(f"inspect.getframeinfo(prev_frame): {inspect.getframeinfo(prev_frame)}")

        print('\n\n')
        print(hex(id(cur_frame)))
        print(f"repr(cur_frame): {repr(cur_frame)}")
        print(f"cur frame {cur_frame}")
        print(f"cur_frame.f_locals {cur_frame.f_locals}", end='\n')
        print(f"dir(cur_frame) {dir(cur_frame)}", end='\n')
        print(f"cur.f_code.co_nam {cur_frame.f_code.co_name}", end='\n')
        print(f"inspect.getframeinfo(cur_frame): {inspect.getframeinfo(cur_frame)}")

        cur_call_repr = f"{hex(id(cur_frame))}:{func.__name__}{args}"
        G.add_node(f"{cur_call_repr}")

        # if not coming from main context, build edge
        if prev_frame.f_locals.get('__name__') != '__main__':

            # Construct arguments from previous stack frame

            prev_args = tuple(arg[1] for arg in prev_frame.f_locals.items())
            print(f"prev_args: {prev_args}")

            prev_call_repr = f"{hex(id(prev_frame))}:{prev_frame.f_code.co_name}{prev_args}"

            G.add_edge(prev_call_repr, cur_call_repr)

        out = func(*args, **kwargs)


        return out

    return inner

def draw():
    """FIXME: add docstring"""
    nx.draw(
        G,
        with_labels=True,
        node_color='skyblue',
        node_size=700,
        font_size=16,
        font_color='black',
        edge_color='gray'
    )

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
