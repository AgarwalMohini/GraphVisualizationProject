def get_sample_graph():
    return {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 4, 'C': 1, 'G': 7},
        'G': {}
    }