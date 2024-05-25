"""Recursion visualization toolkit"""
import inspect
import time

import networkx as nx

G = nx.DiGraph()

def generate_node_fingerprint(frame, fn, args, ts):
    """Generate a unique fingerprint for a given function call"""
    addr = hex(id(frame))
    fn_label = fn+str(args)
    return {
        "node_for_adding":f"{addr}.{fn_label}.{str(ts)}",
        "label": fn_label,
        "addr": addr,
        "ts": ts
    }

def visualize(func):
    """Decorator for visualization of recursive calls"""

    def inner(*args, **kwargs):
        # function signature for traceability
        fn_timestamp = time.time_ns()

        cur_frame = inspect.currentframe()
        prev_frame = cur_frame.f_back

        cur_fingerprint = generate_node_fingerprint(
            cur_frame, func.__name__, args, fn_timestamp
        )
        G.add_node(**cur_fingerprint)

        # if not coming from main context, build edge
        if prev_frame.f_locals.get('__name__') != '__main__':
            prev_wrapped_frame = prev_frame.f_back

            # Construct representation from previous stack frame
            prev_wrapped_fingerprint = generate_node_fingerprint(
                prev_wrapped_frame,
                prev_frame.f_code.co_name,
                prev_wrapped_frame.f_locals['args'],
                prev_wrapped_frame.f_locals['fn_timestamp']
            )

            G.add_edge(
                prev_wrapped_fingerprint["node_for_adding"],
                cur_fingerprint["node_for_adding"]
            )

        return func(*args, **kwargs)

    return inner
