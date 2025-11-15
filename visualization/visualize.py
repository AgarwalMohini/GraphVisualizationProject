# import matplotlib.pyplot as plt
# import networkx as nx

# def setup_plot(fig, G, pos, title="Graph Traversal"):
#     fig.clear()
#     ax1 = fig.add_subplot(1, 2, 1)
#     ax2 = fig.add_subplot(1, 2, 2)
#     ax1.set_title(title, fontsize=14)
#     ax2.set_title("Steps", fontsize=14)
#     ax2.axis("off")
    
#     # Draw initial state of the graph
#     nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, font_size=12, font_weight="bold", ax=ax1)
#     labels = nx.get_edge_attributes(G, 'weight')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax1)
    
#     return ax1, ax2

# def update_plot(fig, canvas, ax1, ax2, G, pos, result_text, highlight_nodes=None, highlight_edges=None, current_node=None):
#     ax1.clear()
#     ax1.set_title(ax1.get_title(), fontsize=14)
    
#     node_colors = []
#     for node in G.nodes():
#         if node == current_node:
#             node_colors.append("red")
#         elif node in highlight_nodes:
#             node_colors.append("lightgreen")
#         else:
#             node_colors.append("skyblue")

#     nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=12, font_weight="bold", ax=ax1)
#     labels = nx.get_edge_attributes(G, 'weight')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax1)
    
#     if highlight_edges:
#         nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color="red", width=2, ax=ax1)
    
#     ax2.clear()
#     ax2.set_title("Steps", fontsize=14)
#     ax2.axis("off")
#     ax2.text(0.05, 0.95, result_text, fontsize=12, va="top", wrap=True)
#     canvas.draw_idle()

import matplotlib.pyplot as plt
import networkx as nx

def setup_plot(fig, G, pos, title="Graph Traversal"):
    fig.clear()
    
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # Title for graph area
    ax1.set_title(title, fontsize=14)

    # Steps panel
    ax2.set_title("Steps", fontsize=14)
    ax2.axis("off")

    # Draw initial graph
    nx.draw(
        G, pos,
        with_labels=True,
        node_color="skyblue",
        node_size=1500,
        font_size=12,
        font_weight="bold",
        ax=ax1
    )
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax1)

    return ax1, ax2


def update_plot(
    fig, canvas, ax1, ax2, G, pos, result_text,
    highlight_nodes=None,
    highlight_edges=None,
    current_node=None,
    path_nodes=None,          # NEW for A*
    matrix=None               # NEW for Floyd–Warshall
):
    ax1.clear()

    # Keep existing title
    ax1.set_title(ax1.get_title(), fontsize=14)

    # ----------------------------------
    # NODE COLOR SYSTEM
    # ----------------------------------
    node_colors = []
    for node in G.nodes():
        if path_nodes and node in path_nodes:
            node_colors.append("yellow")      # Path from A*
        elif node == current_node:
            node_colors.append("red")         # Current node
        elif highlight_nodes and node in highlight_nodes:
            node_colors.append("lightgreen")  # Visited / in frontier
        else:
            node_colors.append("skyblue")     # Default

    # Draw graph
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=1500,
        font_size=12,
        font_weight="bold",
        ax=ax1
    )
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax1)

    # Highlight edges if needed
    if highlight_edges:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=highlight_edges,
            edge_color="red",
            width=2,
            ax=ax1
        )

    # ----------------------------------
    # RIGHT PANEL (STEPS)
    # ----------------------------------
    ax2.clear()
    ax2.set_title("Steps", fontsize=14)
    ax2.axis("off")

    # If Floyd–Warshall matrix is supplied, render matrix text
    if matrix:
        text = ""
        for row in matrix:
            text += "  ".join([f"{x:4}" for x in row]) + "\n"
        result_text += "\n\nDistance Matrix:\n" + text

    # Display text
    ax2.text(0.05, 0.95, result_text, fontsize=12, va="top", wrap=True)

    # Redraw canvas
    canvas.draw_idle()
