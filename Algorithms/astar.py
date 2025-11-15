import math
import heapq
import networkx as nx
from visualization.visualize import setup_plot, update_plot

class AStar_Visualizer:
    def __init__(self, graph_dict, start, goal, fig, canvas, button):
        self.graph = graph_dict
        self.start = start     
        self.goal = goal
        self.fig = fig
        self.canvas = canvas
        self.button = button

        # Build graph
        self.G = nx.Graph()
        for u, nbrs in self.graph.items():
            for v, w in nbrs.items():
                self.G.add_edge(u, v, weight=w)

        # stabilize layout
        self.pos = nx.spring_layout(self.G, iterations=50)

        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="A* Search")
        self.button.config(command=self.reset_and_run)

        self.reset_and_run()

    def heuristic(self, a, b):
        ax, ay = self.pos[a]
        bx, by = self.pos[b]
        return math.dist((ax, ay), (bx, by))

    def reconstruct_path(self):
        path = [self.goal]
        current = self.goal
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)
        return list(reversed(path))

    def run_step(self):

        if not self.open_heap:
            update_plot(self.fig, self.canvas, self.ax1, self.ax2,
                        self.G, self.pos,
                        "No path found.",
                        highlight_nodes=self.closed_set)
            return

        f, node = heapq.heappop(self.open_heap)

        if node in self.closed_set:
            self.fig.canvas.get_tk_widget().after(200, self.run_step)
            return

        self.closed_set.add(node)
        self.processed_order.append(node)

        # display info
        open_nodes = " -> ".join([str(n) for _, n in self.open_heap]) or "Empty"

        result_text = (
            f"Processing: {node}\n\n"
            f"Open List:\n{open_nodes}\n\n"
            f"Processed:\n{' -> '.join(self.processed_order)}"
        )

        update_plot(self.fig, self.canvas, self.ax1, self.ax2,
                    self.G, self.pos, result_text,
                    highlight_nodes=self.closed_set,
                    current_node=node)

        # goal reached
        if node == self.goal:
            path = self.reconstruct_path()
            edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            update_plot(self.fig, self.canvas, self.ax1, self.ax2,
                        self.G, self.pos,
                        "Path found:\n" + " -> ".join(path),
                        highlight_nodes=set(path),
                        highlight_edges=edges,
                        current_node=self.goal)
            return

        # explore neighbors
        for neigh, w in self.graph[node].items():
            tentative = self.g_score[node] + w
            if tentative < self.g_score.get(neigh, float('inf')):
                self.came_from[neigh] = node
                self.g_score[neigh] = tentative
                f = tentative + self.heuristic(neigh, self.goal)
                heapq.heappush(self.open_heap, (f, neigh))

        self.fig.canvas.get_tk_widget().after(700, self.run_step)

    def reset_and_run(self):
        self.g_score = {n: float('inf') for n in self.G.nodes()}
        self.g_score[self.start] = 0

        self.came_from = {}
        self.closed_set = set()
        self.processed_order = []
        self.f_score = {}

        self.open_heap = [(self.heuristic(self.start, self.goal), self.start)]

        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="A* Search")
        update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, "Starting A* ...")

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.run_step()


def visualize_astar(graph_dict, start, goal, fig, canvas, button):
    AStar_Visualizer(graph_dict, start, goal, fig, canvas, button)
