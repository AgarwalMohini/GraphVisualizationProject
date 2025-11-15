import networkx as nx
from visualization.visualize import setup_plot, update_plot
import copy

class FloydWarshall_Visualizer:
    def __init__(self, graph_dict, fig, canvas, button):
        self.graph = graph_dict
        self.fig = fig
        self.canvas = canvas
        self.button = button

        # use directed graph to capture direction if present, but treat it generally
        self.G = nx.DiGraph()
        for u, nbrs in self.graph.items():
            for v, w in nbrs.items():
                self.G.add_edge(u, v, weight=w)
        self.pos = nx.spring_layout(self.G)

        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Floyd–Warshall (All-Pairs)")
        self.button.config(command=self.reset_and_run)

        self.reset_and_run()

    def run_step(self):
        # process one full k iteration at a time (keeps UI responsive & readable)
        if self.k_index >= len(self.nodes):
            # finished
            lines = []
            for i in self.nodes:
                for j in self.nodes:
                    d = self.dist[i][j]
                    lines.append(f"{i}->{j}: {'inf' if d == float('inf') else d}")
            update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos,
                        "Final distance matrix:\n" + "\n".join(lines),
                        highlight_nodes=set(self.nodes))
            return

        k = self.nodes[self.k_index]
        # update distances via node k
        for i in self.nodes:
            for j in self.nodes:
                if self.dist[i][k] != float('inf') and self.dist[k][j] != float('inf'):
                    if self.dist[i][j] > self.dist[i][k] + self.dist[k][j]:
                        self.dist[i][j] = self.dist[i][k] + self.dist[k][j]

        # display summary after finishing with this k
        matrix_lines = []
        for i in self.nodes:
            row = []
            for j in self.nodes:
                d = self.dist[i][j]
                row.append('inf' if d == float('inf') else str(d))
            matrix_lines.append(f"{i}: " + ", ".join(row))

        result_text = f"After considering intermediate node k = {k}:\n" + "\n".join(matrix_lines)
        update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, result_text,
                    highlight_nodes={k})

        self.k_index += 1
        self.fig.canvas.get_tk_widget().after(1000, self.run_step)

    def reset_and_run(self):
        self.nodes = list(self.G.nodes())
        # initialize distance matrix
        self.dist = {i: {j: float('inf') for j in self.nodes} for i in self.nodes}
        for n in self.nodes:
            self.dist[n][n] = 0
        for u, v, d in self.G.edges(data=True):
            self.dist[u][v] = d['weight']

        self.k_index = 0
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Floyd–Warshall (All-Pairs)")
        self.run_step()

def visualize_floyd_warshal(graph_dict, fig, canvas, button):
    FloydWarshall_Visualizer(graph_dict, fig, canvas, button)
