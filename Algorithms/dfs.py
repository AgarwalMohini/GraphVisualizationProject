import networkx as nx
import matplotlib.pyplot as plt
from visualization.visualize import setup_plot, update_plot

class DFS_Visualizer:
    def __init__(self, graph_dict, start, fig, canvas, button):
        self.graph_dict = graph_dict
        self.start = start
        self.fig = fig
        self.canvas = canvas
        self.button = button

        self.G = nx.Graph()
        for u, neighbors in self.graph_dict.items():
            for v, w in neighbors.items():
                self.G.add_edge(u, v, weight=w)
        self.pos = nx.spring_layout(self.G)
        
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="DFS Traversal")
        self.button.config(command=self.reset_and_run)
        
        self.reset_and_run()

    def run_step(self):
        if not self.stack:
            update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, "Final DFS Order:\n" + " -> ".join(self.visited), highlight_nodes=set(self.visited))
            return
            
        node = self.stack.pop()
        if node not in self.visited:
            self.visited.append(node)
            
            result_text = "DFS Order:\n" + " -> ".join(self.visited)
            update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, result_text, highlight_nodes=set(self.visited), current_node=node)
            
            for neighbor in reversed(list(self.graph_dict[node].keys())):
                if neighbor not in self.visited:
                    self.stack.append(neighbor)
        
        self.fig.canvas.get_tk_widget().after(1000, self.run_step)

    def reset_and_run(self):
        self.stack = [self.start]
        self.visited = []
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="DFS Traversal")
        self.run_step()

def visualize_dfs(graph_dict, start, fig, canvas, button):
    DFS_Visualizer(graph_dict, start, fig, canvas, button)