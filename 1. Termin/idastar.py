import networkx as nx
import matplotlib.pyplot as plt
import math
import time

G = nx.Graph()

# Knoten mit Positionen (x, y)
positions = {
    'A': (0, 0),
    'B': (1, 2),
    'C': (4, 1),
    'D': (5, 3),
    'E': (7, 0)
}

# Knoten hinzufügen
for node, pos in positions.items():
    G.add_node(node, pos=pos)

# Kanten (mit Kosten)
G.add_edge('A', 'B', weight=2.2)
G.add_edge('A', 'C', weight=4.1)
G.add_edge('B', 'D', weight=3.0)
G.add_edge('C', 'D', weight=2.5)
G.add_edge('D', 'E', weight=2.2)

startnode = 'A'
targetnode = 'E'
path = []

def idastar(startnode):
    start_time = time.time()
    threshold = heuristic(startnode)
    expanded_nodes = 0

    while(1):
        temp, expanded_nodes = search(startnode, 0, threshold, expanded_nodes)
        if temp == 'FOUND':
            end_time = time.time()
            actual_time = end_time - start_time
            return path, actual_time, expanded_nodes
        
        if(temp == float('inf')):
            return
        
        threshold = temp
    end_time = time.time()
    actual_time = end_time - start_time
    return None, actual_time, expanded_nodes

# IDA* Funktionen
def search(node, g, treshold, expanded_nodes):
    expanded_nodes += 1
    f = g + heuristic(node)

    if f > treshold:
        return f, expanded_nodes
    
    if node == targetnode:
        path.append(node)
        return 'FOUND', expanded_nodes
    
    #infinity
    min = float('inf')

    for tempnode, weight in neighbors(node):
        path.append(node)
        temp, expanded_nodes = search(tempnode, g + weight, treshold, expanded_nodes)
        if temp == 'FOUND':
            return 'FOUND', expanded_nodes
        path.pop()
        if temp < min:
            min = temp
    return min, expanded_nodes

def neighbors(state):
    return [(n, G[state][n]['weight']) for n in G.neighbors(state)]

def heuristic(state):
    x1, y1 = G.nodes[state]['pos']
    x2, y2 = G.nodes[targetnode]['pos']
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # Luftlinie

""" def create_grid(size):
    G = nx.grid_2d_graph(size, size)

    # alle Kanten Gewicht = 1
    for (u, v) in G.edges():
        G[u][v]['weight'] = 1

    return G

def heuristic(state):
    x1, y1 = state
    x2, y2 = targetnode
    return abs(x1 - x2) + abs(y1 - y2)  # Manhattan-Distanz 

G = create_grid(20)
startnode = (0, 0)
targetnode = (19, 19)"""

if __name__ == "__main__":
    path, actual_time, expanded_nodes = idastar(startnode)

    print(f"Pfad: {path}\nBenötigte Zeit: {actual_time * 1000:.3f} Millisekunden\nExpandierte Knoten: {expanded_nodes}")