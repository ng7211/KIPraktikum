import networkx as nx
import matplotlib.pyplot as plt
import math

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
    threshold = heuristic(startnode)

    while(1):
        temp = search(startnode, 0, threshold)
        if temp == 'FOUND':
            return path
        
        if(temp == float('inf')):
            return
        
        threshold = temp



def search(node, g, treshold):
    f = g + heuristic(node)

    if f > treshold:
        return f
    
    if node == targetnode:
        path.append(node)
        return 'FOUND'
    
    #infinity
    min = float('inf')

    for tempnode, weight in neighbors(node):
        path.append(node)
        temp = search(tempnode, g + weight, treshold)
        if temp == 'FOUND':
            return 'FOUND'
        path.pop()
        if temp < min:
            min = temp
    return min


def heuristic(state):
    x1, y1 = G.nodes[state]['pos']
    x2, y2 = G.nodes[targetnode]['pos']
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # Luftlinie

def neighbors(state):
    return [(n, G[state][n]['weight']) for n in G.neighbors(state)]

if __name__ == "__main__":
    path = idastar(startnode)

    print("Pfad:", path)