#a star search implementation using class and objects in python

class Graph:
    def __init__(self):
        self.adj = {}   # node -> list of (neighbour, cost)
        self.h = {}     # straight line distance of every node to Bucharest

    # add an undirected road between u and v
    def addEdge(self, u, v, cost):
        if u not in self.adj:
            self.adj[u] = []

        if v not in self.adj:
            self.adj[v] = []

        self.adj[u].append((v, cost))
        self.adj[v].append((u, cost))

    # store the heuristic value of a node
    def addHeuristic(self, node, value):
        self.h[node] = value

    # a star search from start to goal, f(n) = g(n) + h(n)
    def AStar(self, start, goal):

        # every item stores node, g, f and the path taken
        open_list = [[start, 0, self.h[start], [start]]]

        closed = []
        expanded = 0

        print(f"A* Search from {start} to {goal}")
        print()

        while len(open_list) > 0:

            # pick the node with the smallest f value
            best = 0
            for i in range(1, len(open_list)):
                if open_list[i][2] < open_list[best][2]:
                    best = i

            node, g_cost, f_cost, path = open_list[best]
            del open_list[best]

            # already expanded, skip it
            if node in closed:
                continue

            closed.append(node)
            expanded = expanded + 1
            print(f"Expand {node}: g = {g_cost}, h = {self.h[node]}, f = {f_cost}")

            # stop as soon as the goal is reached
            if node == goal:
                print()
                print("Goal reached !")
                print("Final Path:", " -> ".join(path))
                print("Total cost:", g_cost)
                print("Nodes expanded:", expanded)
                return

            # every successor gets a new g value and a new f value
            for neighbour, cost in self.adj[node]:
                if neighbour not in closed:
                    new_g = g_cost + cost
                    new_f = new_g + self.h[neighbour]
                    open_list.append([neighbour, new_g, new_f, path + [neighbour]])

        print("Goal not found")


# Bucharest map given in the manual
road = Graph()

road.addEdge('Oradea', 'Zerind', 71)
road.addEdge('Zerind', 'Arad', 75)
road.addEdge('Arad', 'Sibiu', 140)
road.addEdge('Arad', 'Timisoara', 118)
road.addEdge('Timisoara', 'Lugoj', 111)
road.addEdge('Lugoj', 'Mehadia', 70)
road.addEdge('Mehadia', 'Dobreta', 75)
road.addEdge('Dobreta', 'Craiova', 120)
road.addEdge('Craiova', 'Pitesti', 138)
road.addEdge('Craiova', 'Rimnicu Vilcea', 146)
road.addEdge('Sibiu', 'Fagaras', 99)
road.addEdge('Sibiu', 'Rimnicu Vilcea', 80)
road.addEdge('Sibiu', 'Oradea', 151)
road.addEdge('Rimnicu Vilcea', 'Pitesti', 97)
road.addEdge('Pitesti', 'Bucharest', 101)
road.addEdge('Fagaras', 'Bucharest', 211)
road.addEdge('Bucharest', 'Giurgiu', 90)
road.addEdge('Bucharest', 'Urziceni', 85)
road.addEdge('Urziceni', 'Hirsova', 98)
road.addEdge('Urziceni', 'Vaslui', 142)
road.addEdge('Hirsova', 'Eforie', 86)
road.addEdge('Vaslui', 'Iasi', 92)
road.addEdge('Iasi', 'Neamt', 87)

# straight line distance of every city to Bucharest
road.addHeuristic('Arad', 366)
road.addHeuristic('Bucharest', 0)
road.addHeuristic('Craiova', 160)
road.addHeuristic('Dobreta', 242)
road.addHeuristic('Eforie', 161)
road.addHeuristic('Fagaras', 176)
road.addHeuristic('Giurgiu', 77)
road.addHeuristic('Hirsova', 151)
road.addHeuristic('Iasi', 226)
road.addHeuristic('Lugoj', 244)
road.addHeuristic('Mehadia', 241)
road.addHeuristic('Neamt', 234)
road.addHeuristic('Oradea', 380)
road.addHeuristic('Pitesti', 100)
road.addHeuristic('Rimnicu Vilcea', 193)
road.addHeuristic('Sibiu', 253)
road.addHeuristic('Timisoara', 329)
road.addHeuristic('Urziceni', 80)
road.addHeuristic('Vaslui', 199)
road.addHeuristic('Zerind', 374)

# find a path from Arad to Bucharest
road.AStar('Arad', 'Bucharest')
