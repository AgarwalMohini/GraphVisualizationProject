import networkx as nx
import matplotlib.pyplot as plt
from visualization.visualize import setup_plot, update_plot

class Kruskals_Visualizer:
    def __init__(self, graph_dict, fig, canvas, button):
        self.graph_dict = graph_dict
        self.fig = fig
        self.canvas = canvas
        self.button = button
        
        self.G = nx.Graph()
        for u, neighbors in self.graph_dict.items():
            for v, w in neighbors.items():
                if not self.G.has_edge(u, v):
                    self.G.add_edge(u, v, weight=w)
        self.pos = nx.spring_layout(self.G)
        
        self.edges = sorted([(u, v, d['weight']) for u, v, d in self.G.edges(data=True)], key=lambda x: x[2])
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Kruskal's Algorithm")
        self.button.config(command=self.reset_and_run)
        
        self.reset_and_run()

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def run_step(self):
        if self.edge_index >= len(self.edges) or len(self.mst_edges) == len(self.G.nodes()) - 1:
            update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, "Final MST Edges:\n" + "\n".join([f"{a}-{b}" for a, b in self.mst_edges]), highlight_nodes=[n for e in self.mst_edges for n in e], highlight_edges=self.mst_edges)
            return
            
        u, v, w = self.edges[self.edge_index]
        self.edge_index += 1
        
        root_u = self.find(u)
        root_v = self.find(v)
        
        if root_u != root_v:
            self.mst_edges.append((u, v))
            self.parent[root_u] = root_v

        result_text = "Considering Edge:\n" + f"{u}-{v} (Weight: {w})"
        result_text += "\n\nMST Edges:\n" + "\n".join([f"{a}-{b}" for a, b in self.mst_edges])
        update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, result_text, highlight_nodes=[n for e in self.mst_edges for n in e], highlight_edges=[(u, v)])
        
        self.fig.canvas.get_tk_widget().after(1000, self.run_step)

    def reset_and_run(self):
        self.parent = {node: node for node in self.G.nodes()}
        self.mst_edges = []
        self.edge_index = 0
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Kruskal's Algorithm")
        self.run_step()

def visualize_kruskals(graph_dict, fig, canvas, button):
    Kruskals_Visualizer(graph_dict, fig, canvas, button)