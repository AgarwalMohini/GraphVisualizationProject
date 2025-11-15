import networkx as nx
from collections import deque
from visualization.visualize import setup_plot, update_plot

class TopoSort_Visualizer:
    def __init__(self, graph_dict, fig, canvas, button):
        # topological sort is for directed graphs (DAG)
        self.graph = graph_dict
        self.fig = fig
        self.canvas = canvas
        self.button = button

        self.G = nx.DiGraph()
        for u, nbrs in self.graph.items():
            for v, w in nbrs.items():
                # weight isn't required for topo, but preserve if present
                self.G.add_edge(u, v, weight=w)
        self.pos = nx.spring_layout(self.G)

        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Topological Sort (Kahn's Algorithm)")
        self.button.config(command=self.reset_and_run)

        self.reset_and_run()

    def run_step(self):
        if not self.queue:
            if len(self.order) == len(self.G.nodes()):
                update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos,
                            "Topological Order:\n" + " -> ".join(self.order),
                            highlight_nodes=set(self.order))
            else:
                update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos,
                            "Graph has a cycle — topological ordering not possible.",
                            highlight_nodes=set(self.order))
            return

        node = self.queue.popleft()
        self.order.append(node)

        # Visual update
        result_text = "Removed Node (zero indegree): " + node + "\n\n"
        result_text += "Current Order:\n" + " -> ".join(self.order) + "\n\n"
        result_text += "Queue:\n" + " -> ".join(list(self.queue))
        update_plot(self.fig, self.canvas, self.ax1, self.ax2, self.G, self.pos, result_text,
                    highlight_nodes=set(self.order), current_node=node)

        for neigh in self.graph.get(node, {}).keys():
            self.indegree[neigh] -= 1
            if self.indegree[neigh] == 0:
                self.queue.append(neigh)

        self.fig.canvas.get_tk_widget().after(1000, self.run_step)

    def reset_and_run(self):
        # compute indegrees
        self.indegree = {n: 0 for n in self.G.nodes()}
        for u in self.graph:
            for v in self.graph[u].keys():
                self.indegree[v] += 1

        # initialize queue with 0 indegree nodes
        self.queue = deque([n for n in self.G.nodes() if self.indegree[n] == 0])
        self.order = []

        self.ax1, self.ax2 = setup_plot(self.fig, self.G, self.pos, title="Topological Sort (Kahn's Algorithm)")
        self.run_step()

def visualize_topological_sort(graph_dict, fig, canvas, button):
    TopoSort_Visualizer(graph_dict, fig, canvas, button)
