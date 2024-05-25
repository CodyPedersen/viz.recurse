"""Toolkit for outputing graph in multiple formats"""
import json
import networkx as nx
import matplotlib.pyplot as plt

from networkx.drawing.nx_pydot import graphviz_layout

from .vizzy import G


def draw(font_size=8, gv_layout="dot", arrow_size=7, node_size=70) -> None:
    """Draw recursive tree/list from captured graph"""
    pos = graphviz_layout(G, prog=gv_layout)
    labels = {node: data['label'] for node, data in G.nodes(data=True)}

    nx.draw_networkx_nodes(G, pos, node_size=node_size)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='-|>', arrowsize=arrow_size)
    nx.draw_networkx_labels(G, pos, font_size=font_size, font_family='sans-serif', labels=labels)

    plt.show()


def graph_repr() -> dict:
    """Returns a dict representation of the call graph"""

    labels = {node: data['label'] for node, data in G.nodes(data=True)}

    # Format nodes and edges to distinct variation
    nodes = [f"{k}" for k,_ in labels.items()]
    edges = [(src, dest) for src, dest in G.edges()]

    return {
        "nodes": nodes,
        "edges": edges
    }


def dump_graph(fileloc='./graph.json') -> None:
    """Dump graph callstack to a local file"""
    graph = graph_repr()

    with open(fileloc, 'w', encoding='utf8') as f:
        json.dump(graph, f)
