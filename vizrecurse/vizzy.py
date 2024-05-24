"""Recursion visualization toolkit"""
import inspect

import networkx as nx

G = nx.DiGraph()


def visualize(func):
    """Decorator for visualization of recursive calls"""

    def inner(*args, **kwargs):
        cur_frame = inspect.currentframe()
        prev_frame = cur_frame.f_back

        # Build current node representation
        cur_addr = hex(id(cur_frame))
        label = func.__name__+str(args)
        cur_repr = cur_addr + '.' + label
        G.add_node(cur_repr, label=label)
        print(G.nodes(data=True))

        # if not coming from main context, build edge
        if prev_frame.f_locals.get('__name__') != '__main__':
            prev_wrapped_frame = prev_frame.f_back

            # Construct representation from previous stack frame
            prev_wrapped_addr = hex(id(prev_wrapped_frame))
            prev_fn = prev_frame.f_code.co_name
            prev_args = prev_wrapped_frame.f_locals['args']
            prev_wrapped_repr = f"{prev_wrapped_addr}.{prev_fn}{prev_args}"
            G.add_edge(prev_wrapped_repr, cur_repr)

        return func(*args, **kwargs)

    return inner
