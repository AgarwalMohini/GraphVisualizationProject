import networkx as nx
import matplotlib.pyplot as plt
import heapq
from visualization.visualize import setup_plot, update_plot

class Prims_Visualizer:
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
        
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Prim's Algorithm")
        self.button.config(command=self.reset_and_run)
        
        self.reset_and_run()

    def run_step(self):
        # We use a loop to ensure a step is processed even if the first pop is an already visited node
        while self.min_heap:
            weight, u, v = heapq.heappop(self.min_heap)
            if v not in self.visited:
                self.visited.add(v)
                self.mst_edges.append((u, v))
                
                result_text = "MST Edges:\n" + "\n".join([f"{a}-{b}" for a, b in self.mst_edges])
                update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, result_text, highlight_nodes=self.visited, highlight_edges=[(u, v)], current_node=v)
                
                for neighbor, w in self.graph_dict.get(v, {}).items():
                    if neighbor not in self.visited:
                        heapq.heappush(self.min_heap, (w, v, neighbor))
                
                self.fig.canvas.get_tk_widget().after(1000, self.run_step)
                return

        # If the loop finishes without processing a new step, it means the heap is exhausted.
        if len(self.visited) >= len(self.graph_dict):
             update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, "Final MST Edges:\n" + "\n".join([f"{a}-{b}" for a, b in self.mst_edges]), highlight_nodes=self.visited, highlight_edges=self.mst_edges)
             return

        # If we didn't return, it means we popped an already visited node and should try again.
        self.fig.canvas.get_tk_widget().after(100, self.run_step)


    def reset_and_run(self):
        self.mst_edges = []
        self.visited = {self.start}
        self.min_heap = [(weight, self.start, neighbor) for neighbor, weight in self.graph_dict.get(self.start, {}).items()]
        heapq.heapify(self.min_heap)
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Prim's Algorithm")
        self.run_step()

def visualize_prims(graph_dict, start, fig, canvas, button):
    Prims_Visualizer(graph_dict, start, fig, canvas, button)