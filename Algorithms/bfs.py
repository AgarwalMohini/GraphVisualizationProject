import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from visualization.visualize import setup_plot, update_plot
class BFS_Visualizer:
    def __init__(self, graph, start, fig, canvas, button):
        self.graph = graph
        self.start = start
        self.fig = fig
        self.canvas = canvas
        self.button = button
        
        self.G = nx.Graph()
        for u, neighbors in self.graph.items():
            for v, w in neighbors.items():
                self.G.add_edge(u, v, weight=w)
        self.pos = nx.spring_layout(self.G)
        
        self.queue = deque()
        self.visited = set()
        self.traversal_order = []
        
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="BFS Traversal")
        self.button.config(command=self.reset_and_run)
        
        # Start the initial visualization
        self.reset_and_run()

    def run_step(self):
        if not self.queue:
            update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, "Final BFS Order:\n" + " -> ".join(self.traversal_order), highlight_nodes=self.visited)
            return

        node = self.queue.popleft()
        if node not in self.visited:
            self.visited.add(node)
            self.traversal_order.append(node)
            
            result_text = "BFS Order:\n" + " -> ".join(self.traversal_order)
            update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, result_text, highlight_nodes=self.visited, current_node=node)
            
            for neighbor in sorted(self.graph[node].keys()):
                if neighbor not in self.visited:
                    self.queue.append(neighbor)
        
        self.fig.canvas.get_tk_widget().after(1000, self.run_step)


    def reset_and_run(self):
        self.queue = deque([self.start])
        self.visited = set()
        self.traversal_order = []
        
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="BFS Traversal")
        
        self.run_step()

def visualize_bfs(graph, start, fig, canvas, button):
    # Instantiate the class to start the visualization
    BFS_Visualizer(graph, start, fig, canvas, button)