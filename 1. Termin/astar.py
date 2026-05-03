import heapq
import networkx as nx
import matplotlib.pyplot as plt
import math
import time

def astar(start, goal_test, neighbors, heuristic):
    start_time = time.time()

    open_list = []
    heapq.heappush(open_list, (heuristic(start), start))

    came_from = {}
    g_cost = {start: 0}
    closed_set = set()

    expanded_nodes = 0

    while open_list:
        f, current = heapq.heappop(open_list)

        if current in closed_set:
            continue

        expanded_nodes += 1

        if goal_test(current):
            endtime = time.time()
            actual_time = endtime - start_time
            path = reconstruct_path(came_from, current)
            return path, actual_time, expanded_nodes # time zurückgeben
        closed_set.add(current)

        for neighbor, cost in neighbors(current):
            if neighbor in closed_set:
                continue

            new_g = g_cost[current] + cost

            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = new_g

                f_cost = new_g + heuristic(neighbor)
                heapq.heappush(open_list, (f_cost, neighbor))

    # wenn kein pfad gefunden wurde
    endtime = time.time()
    actual_time = endtime - start_time
    return None, actual_time, expanded_nodes  # time zurückgeben


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


# Graph erstellen

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


# Start & Ziel

start = 'A'
goal = 'E'


# A*-Funktionen

def goal_test(state):
    return state == goal

def neighbors(state):
    return [(n, G[state][n]['weight']) for n in G.neighbors(state)]

def heuristic(state):
    x1, y1 = G.nodes[state]['pos']
    x2, y2 = G.nodes[goal]['pos']
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # Luftlinie


# Test

if __name__ == "__main__":
    path, actual_time, nodes = astar(start, goal_test, neighbors, heuristic)

    print("Pfad:", path)
    print("Expandierte Knoten:", nodes)
    print(f"Benötigte Zeit: {actual_time * 1000:.3f} Millisekunden")