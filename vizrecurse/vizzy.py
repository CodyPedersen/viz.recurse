# pylint: disable=invalid-name, import-error
"""Recursion visualization toolkit"""
import inspect
import time

from types import FrameType
from typing import Callable, ParamSpec, TypeVar

import networkx as nx

G = nx.DiGraph()

Param = ParamSpec("Param")
RetType = TypeVar("RetType")

def generate_node_fingerprint(
    frame: FrameType,
    fn: str,
    arg_str: str,
    ts: int
    ) -> dict[str,int|str]:
    """Generate a unique fingerprint for a given function call"""
    addr = hex(id(frame))
    fn_label = fn+arg_str
    return {
        "node_for_adding":f"{addr}.{fn_label}.{str(ts)}",
        "label": fn_label,
        "addr": addr,
        "ts": ts
    }


def visualize(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
    """Decorator for visualization of recursive calls"""

    def inner(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
        # function signature for traceability
        fn_timestamp = time.time_ns()

        cur_frame = inspect.currentframe()
        if not cur_frame:
            raise ValueError("Unable to infer existing frame.")

        prev_frame = cur_frame.f_back
        if not prev_frame:
            raise ValueError("Unable to infer previous frame.")

        cur_fingerprint = generate_node_fingerprint(
            cur_frame, func.__name__, str(args), fn_timestamp
        )
        G.add_node(**cur_fingerprint)

        # We've hit module frame context
        if prev_frame.f_code.co_name == '<module>':
            return func(*args, **kwargs)

        # Get parent wrapped frame
        prev_wrapped_frame = prev_frame.f_back
        if not prev_wrapped_frame:
            raise ValueError("Wrapper frame not found. Validate frame context.")

        # If in wrapper frame context, add edge
        if prev_wrapped_frame.f_code.co_name == cur_frame.f_code.co_name:

            # Construct representation from previous stack frame
            prev_wrapped_fingerprint = generate_node_fingerprint(
                prev_wrapped_frame,
                prev_frame.f_code.co_name,
                str(prev_wrapped_frame.f_locals['args']),
                prev_wrapped_frame.f_locals['fn_timestamp']
            )

            G.add_edge(
                prev_wrapped_fingerprint["node_for_adding"],
                cur_fingerprint["node_for_adding"]
            )

        return func(*args, **kwargs)

    return inner
