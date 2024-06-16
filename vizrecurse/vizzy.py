# pylint: disable=invalid-name, import-error
"""Recursion visualization toolkit"""
import inspect
import sys
import time

from types import FrameType
from typing import (
    Any,
    Concatenate,
    Callable,
    Optional,
    ParamSpec,
    TypeVar
)
from typing_extensions import TypeAlias

import networkx as nx

G = nx.DiGraph()

Param = ParamSpec("Param")
RetType = TypeVar("RetType")
TraceFunction: TypeAlias = 'Callable[[FrameType, str, Any], Optional[TraceFunction]]'


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


def get_frame_set(
    frame: Optional[FrameType]
) -> tuple[Optional[FrameType], Optional[FrameType]]:
    """Capture current and prior frameset"""

    cur_frame = frame

    # unable to locate prior frame state
    if not frame or frame.f_code.co_name != 'debugged_func':  # remove hardcode
        return None, None

    # initialize to prior frame
    frame = frame.f_back
    if not frame:
        return frame, None

    # locate last debug frame
    while frame.f_code.co_name != 'debugged_func':  # remove hardcode
        prior_frame = frame.f_back

        if not prior_frame or prior_frame.f_code.co_name == '<module>':
            return cur_frame, None

        frame = prior_frame

    return cur_frame, frame


def visualize(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
    """Test debugging the existing frame"""

    def trace_callback(frame: FrameType, event: str, _: Any) -> TraceFunction:
        """Callback function for system trace"""

        cur_debug_frame, prior_debug_frame = get_frame_set(frame)

        if not cur_debug_frame:
            return trace_callback

        if event == 'call':
            # Add node
            fn_args = str(cur_debug_frame.f_locals['args'])
            print(fn_args)
            cur_fingerprint = generate_node_fingerprint(
                frame, func.__name__, fn_args, frame.f_locals['fn_timestamp']
            )
            print(f"cur_fingerprint {cur_fingerprint}")
            G.add_node(**cur_fingerprint)

            if not prior_debug_frame:
                return trace_callback

            # Add edge
            prev_wrapped_fingerprint = generate_node_fingerprint(
                prior_debug_frame,
                prior_debug_frame.f_locals['func'].__name__,
                str(prior_debug_frame.f_locals['args']),
                prior_debug_frame.f_locals['fn_timestamp']
            )

            G.add_edge(
                prev_wrapped_fingerprint["node_for_adding"],
                cur_fingerprint["node_for_adding"]
            )

        return trace_callback


    def initialize_debug(
            func: Callable[Concatenate[int, Param], RetType]
    ) -> Callable[Param, RetType]:
        """Set trace and inject timestamp to uniquely ID function calls."""

        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            timestamp = time.time_ns()
            sys.settrace(trace_callback)
            res = func(timestamp, *args, **kwargs)
            sys.settrace(None)
            return res
        return wrapper

    @initialize_debug
    def debugged_func(
            fn_timestamp: int, /,
            *args: Param.args,
            **kwargs: Param.kwargs,
        ) -> RetType:
        """Dummy wrapper with injected functionality"""

        res = func(*args, **kwargs)
        return res

    return debugged_func
