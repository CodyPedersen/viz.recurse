# pylint: disable=import-error
"""Toolkit for outputing graph in multiple formats"""
import json
import networkx as nx
import matplotlib.pyplot as plt

from networkx.drawing.nx_pydot import graphviz_layout

from .vizzy import G


def draw(
    font_size: int = 6,
    font_weight: str = "bold",
    gv_layout: str = "dot",
    arrow_size: int = 7,
    node_size: int = 70
    ) -> None:
    """Draw recursive tree/list from captured graph"""

    pos = graphviz_layout(G, prog=gv_layout)
    labels = {node: data['label'] for node, data in G.nodes(data=True)}

    nx.draw_networkx_nodes(G, pos, node_size=node_size)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='-|>', arrowsize=arrow_size)
    nx.draw_networkx_labels(
        G,
        pos,
        font_size=font_size,
        font_weight=font_weight,
        font_family='sans-serif',
        labels=labels,
    )

    plt.show()


def graph_repr() -> dict[str, list[dict[str,str|int]]] | list[list[str]]:
    """Returns a dict representation of the call graph"""

    # Format nodes and edges to distinct variation
    nodes = [data for _, data in G.nodes(data=True)]
    edges = list(G.edges()) #list of tuples

    return {
        "nodes": nodes,
        "edges": edges
    }


def dump_graph(fileloc: str ='./graph.json') -> None:
    """Dump graph callstack to a local file"""
    graph = graph_repr()

    with open(fileloc, 'w', encoding='utf8') as f:
        json.dump(graph, f)
