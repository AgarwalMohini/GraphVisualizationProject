import networkx as nx
from visualization.visualize import setup_plot, update_plot

class BellmanFord_Visualizer:
    def __init__(self, graph_dict, start, fig, canvas, button):
        self.graph = graph_dict
        self.start = start
        self.fig = fig
        self.canvas = canvas
        self.button = button

        # build directed graph representation (weights may be negative)
        self.G = nx.DiGraph()
        for u, nbrs in self.graph.items():
            for v, w in nbrs.items():
                self.G.add_edge(u, v, weight=w)
        self.pos = nx.spring_layout(self.G)

        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Bellman-Ford")
        self.button.config(command=self.reset_and_run)

        self.reset_and_run()

    def run_step(self):
        # iterate over edges in current iteration
        if self.iteration < self.V - 1:
            if self.edge_index >= len(self.edges):
                # finished this iteration
                self.iteration += 1
                self.edge_index = 0
                self.fig.canvas.get_tk_widget().after(200, self.run_step)
                return

            u, v, w = self.edges[self.edge_index]
            self.edge_index += 1

            changed = False
            if self.distance[u] != float('inf') and self.distance[u] + w < self.distance[v]:
                self.distance[v] = self.distance[u] + w
                changed = True

            result_text = f"Iteration {self.iteration + 1}, considering edge {u}->{v} (w={w})\n"
            result_text += "Distances:\n" + "\n".join([f"{n}: {self.distance[n]}" for n in sorted(self.distance.keys())])
            if changed:
                result_text += "\n\nRelaxation performed."
                highlight = {v, u}
            else:
                highlight = {u, v}

            update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, result_text,
                        highlight_nodes=highlight, highlight_edges=[(u, v)])

            self.fig.canvas.get_tk_widget().after(1000, self.run_step)
            return

        # After V-1 iterations, check for negative-weight cycles
        if self.edge_index < len(self.edges):
            u, v, w = self.edges[self.edge_index]
            self.edge_index += 1
            if self.distance[u] != float('inf') and self.distance[u] + w < self.distance[v]:
                update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos,
                            "Negative-weight cycle detected! Relaxation still possible on edge "
                            f"{u}->{v} (w={w})", highlight_nodes={u, v}, highlight_edges=[(u, v)])
                return
            else:
                # continue checking remaining edges
                self.fig.canvas.get_tk_widget().after(200, self.run_step)
                return

        # finished check, output final distances
        final_text = "Final shortest distances (or 'inf'):\n" + "\n".join([f"{n}: {self.distance[n]}" for n in sorted(self.distance.keys())])
        update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, final_text,
                    highlight_nodes={n for n in self.distance if self.distance[n] != float('inf')})
        return

    def reset_and_run(self):
        self.nodes = list(self.G.nodes())
        self.V = len(self.nodes)
        # prepare edge list (u, v, w)
        self.edges = [(u, v, d['weight']) for u, v, d in self.G.edges(data=True)]
        self.distance = {n: float('inf') for n in self.nodes}
        self.distance[self.start] = 0

        self.iteration = 0
        self.edge_index = 0

        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Bellman-Ford")
        self.run_step()

def visualize_bellman_ford(graph_dict, start, fig, canvas, button):
    BellmanFord_Visualizer(graph_dict, start, fig, canvas, button)
