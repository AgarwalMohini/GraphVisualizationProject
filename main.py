# import tkinter as tk
# from tkinter import ttk
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from Core.graph import get_sample_graph
# from Algorithms.bfs import visualize_bfs
# from Algorithms.dfs import visualize_dfs
# from Algorithms.dijkastra import visualize_dijkstra
# from Algorithms.prims import visualize_prims
# from Algorithms.krushkals import visualize_kruskals

# def run_visualization_in_main_thread(algorithm_name, root, frame_right):
#     # Clear previous widgets in the right frame
#     for widget in frame_right.winfo_children():
#         widget.destroy()

#     fig = plt.figure(figsize=(8, 6))
#     canvas = FigureCanvasTkAgg(fig, master=frame_right)
#     canvas_widget = canvas.get_tk_widget()
#     canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#     toolbar = NavigationToolbar2Tk(canvas, frame_right)
#     toolbar.update()
    
#     replay_button = ttk.Button(frame_right, text="Replay")
#     replay_button.pack(side=tk.BOTTOM, pady=10)

#     graph_dict = get_sample_graph()

#     if algorithm_name == "BFS":
#         visualize_bfs(graph_dict, 'A', fig, canvas, replay_button)
#     elif algorithm_name == "DFS":
#         visualize_dfs(graph_dict, 'A', fig, canvas, replay_button)
#     elif algorithm_name == "Dijkstra's Algorithm":
#         visualize_dijkstra(graph_dict, 'A', fig, canvas, replay_button)
#     elif algorithm_name == "Prim's Algorithm":
#         visualize_prims(graph_dict, 'A', fig, canvas, replay_button)
#     elif algorithm_name == "Kruskal's Algorithm":
#         visualize_kruskals(graph_dict, fig, canvas, replay_button)

# def create_gui():
#     root = tk.Tk()
#     root.title("Graph Algorithm Visualizer")
#     root.geometry("1200x800")
    
#     frame_left = ttk.Frame(root, width=300, relief=tk.SUNKEN)
#     frame_right = ttk.Frame(root)
    
#     frame_left.pack(side=tk.LEFT, fill=tk.Y)
#     frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
    
#     label = ttk.Label(frame_left, text="Select an Algorithm", font=("Helvetica", 14))
#     label.pack(pady=20)
    
#     algorithms = ["BFS", "DFS", "Dijkstra's Algorithm", "Prim's Algorithm", "Kruskal's Algorithm"]
    
#     for algo in algorithms:
#         button = ttk.Button(frame_left, text=algo, command=lambda a=algo: run_visualization_in_main_thread(a, root, frame_right))
#         button.pack(pady=5, padx=10, fill=tk.X)
    
#     root.mainloop()

# if __name__ == "__main__":
#     create_gui()


import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from Core.graph import get_sample_graph

# Existing algorithms
from Algorithms.bfs import visualize_bfs
from Algorithms.dfs import visualize_dfs
from Algorithms.dijkastra import visualize_dijkstra
from Algorithms.prims import visualize_prims
from Algorithms.krushkals import visualize_kruskals

# NEW ALGORITHMS
from Algorithms.astar import visualize_astar
from Algorithms.bellman_ford import visualize_bellman_ford
from Algorithms.topological_sort import visualize_topological_sort
from Algorithms.floyd_warshal import visualize_floyd_warshal

def run_visualization_in_main_thread(algorithm_name, root, frame_right):

    for widget in frame_right.winfo_children():
        widget.destroy()

    # === ADD HEADING TITLE HERE ==========================
    heading = ttk.Label(
        frame_right,
        text=algorithm_name,
        font=("Helvetica", 20, "bold"),
        anchor="center"
    )
    heading.pack(pady=10)
    # =====================================================

    fig = plt.figure(figsize=(8, 6))
    canvas = FigureCanvasTkAgg(fig, master=frame_right)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, frame_right)
    toolbar.update()

    replay_button = ttk.Button(frame_right, text="Replay")
    replay_button.pack(side=tk.BOTTOM, pady=10)

    graph_dict = get_sample_graph()

    if algorithm_name == "BFS":
        visualize_bfs(graph_dict, 'A', fig, canvas, replay_button)
    elif algorithm_name == "DFS":
        visualize_dfs(graph_dict, 'A', fig, canvas, replay_button)
    elif algorithm_name == "Dijkstra's Algorithm":
        visualize_dijkstra(graph_dict, 'A', fig, canvas, replay_button)
    elif algorithm_name == "Prim's Algorithm":
        visualize_prims(graph_dict, 'A', fig, canvas, replay_button)
    elif algorithm_name == "Kruskal's Algorithm":
        visualize_kruskals(graph_dict, fig, canvas, replay_button)

    elif algorithm_name == "A* Search":
        visualize_astar(graph_dict, 'A', 'G', fig, canvas, replay_button)
    elif algorithm_name == "Bellman–Ford":
        visualize_bellman_ford(graph_dict, 'A', fig, canvas, replay_button)
    elif algorithm_name == "Topological Sort":
        visualize_topological_sort(graph_dict, fig, canvas, replay_button)
    elif algorithm_name == "Floyd–Warshall":
        visualize_floyd_warshal(graph_dict, fig, canvas, replay_button)



def create_gui():

    root = tk.Tk()
    root.title("Graph Algorithm Visualizer")
    root.geometry("1200x800")

    frame_left = ttk.Frame(root, width=300, relief=tk.SUNKEN)
    frame_right = ttk.Frame(root)

    frame_left.pack(side=tk.LEFT, fill=tk.Y)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    label = ttk.Label(frame_left, text="Select an Algorithm", font=("Helvetica", 14))
    label.pack(pady=20)

    algorithms = [
        "BFS",
        "DFS",
        "Dijkstra's Algorithm",
        "Prim's Algorithm",
        "Kruskal's Algorithm",

        # NEW ---------
        "A* Search",
        "Bellman–Ford",
        "Topological Sort",
        "Floyd–Warshall"
    ]

    for algo in algorithms:
        button = ttk.Button(
            frame_left,
            text=algo,
            command=lambda a=algo: run_visualization_in_main_thread(a, root, frame_right)
        )
        button.pack(pady=5, padx=10, fill=tk.X)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
