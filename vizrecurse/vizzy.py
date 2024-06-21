"""Recursion visualization toolkit"""
import linecache
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

import networkx as nx  # pylint:disable=import-error


Param = ParamSpec("Param")
RetType = TypeVar("RetType")  # pylint: disable=invalid-name
TraceFunction: TypeAlias = 'Callable[[FrameType, str, Any], Optional[TraceFunction]]'

# globals (to be refactored)
G = nx.DiGraph()
container: Optional[str] = None


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
    if not frame or frame.f_code.co_name != container:  # remove hardcode
        return None, None

    # initialize to prior frame
    frame = frame.f_back
    if not frame:
        return frame, None

    # locate last debug frame
    while frame.f_code.co_name != container:  # remove hardcode
        prior_frame = frame.f_back

        if not prior_frame or prior_frame.f_code.co_name == '<module>':
            return cur_frame, None

        frame = prior_frame

    return cur_frame, frame


def visualize(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
    """Test debugging the existing frame"""

    def trace_callback(frame: FrameType, event: str, _: Any) -> TraceFunction:
        """Callback function for system trace"""

        # trace logging for function
        frame_fn = frame.f_code.co_name
        if not frame_fn.startswith('_initializer') and frame_fn != container:
            fname = frame.f_code.co_name

            filename, line_num = frame.f_code.co_filename, frame.f_lineno
            line_code = linecache.getline(filename, line_num).strip()
            if event == 'line':
                execution_log = f"{filename}:{fname}:{line_num} - {line_code}"
                print(execution_log)
            elif event == 'call':
                execution_log = f"{filename}:{line_num} - Called {fname}"
                print(execution_log)

        cur_debug_frame, prior_debug_frame = get_frame_set(frame)

        # short-circuit if not reference frame
        if not cur_debug_frame:
            return trace_callback

        # call event logic
        if event == 'call':
            # Add node
            fn_args = str(cur_debug_frame.f_locals['args'])
            cur_fingerprint = generate_node_fingerprint(
                frame, func.__name__, fn_args, frame.f_locals['fn_timestamp']
            )
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


    def _initializer(
            func: Callable[Concatenate[int, Param], RetType]
    ) -> Callable[Param, RetType]:
        """Set trace and inject timestamp to uniquely ID function calls."""

        global container  # pylint: disable=global-statement
        container = func.__name__

        def _initializer_inner(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            timestamp = time.time_ns()
            sys.settrace(trace_callback)
            res = func(timestamp, *args, **kwargs)
            sys.settrace(None)
            return res

        return _initializer_inner

    @_initializer
    def debugged_func(
            fn_timestamp: int, /,  # pylint: disable=unused-argument
            *args: Param.args,
            **kwargs: Param.kwargs,
        ) -> RetType:
        """
        Dummy wrapper with injected functionality. Used as 
        a fixed reference point for tracking the stack.
        Must be wrapped with initializer decorator to capture 
        first function call & inject fn reference timestamp.
        """

        res = func(*args, **kwargs)

        return res

    return debugged_func
