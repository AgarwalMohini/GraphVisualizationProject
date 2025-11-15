import networkx as nx
import matplotlib.pyplot as plt
import heapq
from visualization.visualize import setup_plot, update_plot

class Dijkstra_Visualizer:
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
        
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Dijkstra's Algorithm")
        self.button.config(command=self.reset_and_run)
        
        self.reset_and_run()

    def run_step(self):
        if not self.pq:
            final_text = "Final Shortest Path Distances:\n" + "\n".join([f"{n}: {d}" for n, d in self.distance.items() if d != float('inf')])
            update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, final_text, highlight_nodes=self.visited)
            return
            
        dist, current_node = heapq.heappop(self.pq)
        if current_node in self.visited:
            self.fig.canvas.get_tk_widget().after(100, self.run_step)
            return
        
        self.visited.add(current_node)
        self.traversal_order.append(current_node)
        
        result_text = f"Processing Node: {current_node}\n"
        result_text += "\nShortest Distances:\n" + "\n".join([f"{n}: {d}" for n, d in self.distance.items() if d != float('inf')])
        result_text += "\n\nVisited Nodes:\n" + " -> ".join(self.traversal_order)
        update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, result_text, highlight_nodes=self.visited, current_node=current_node)

        for neighbor, weight in self.graph[current_node].items():
            if neighbor not in self.visited and dist + weight < self.distance[neighbor]:
                self.distance[neighbor] = dist + weight
                heapq.heappush(self.pq, (self.distance[neighbor], neighbor))
        
        self.fig.canvas.get_tk_widget().after(1000, self.run_step)

    def reset_and_run(self):
        self.distance = {node: float('inf') for node in self.G.nodes()}
        self.distance[self.start] = 0
        self.pq = [(0, self.start)]
        self.visited = set()
        self.traversal_order = []
        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Dijkstra's Algorithm")
        self.run_step()

def visualize_dijkstra(graph, start, fig, canvas, button):
    Dijkstra_Visualizer(graph, start, fig, canvas, button)