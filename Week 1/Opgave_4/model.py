import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # to be used in the A* algorithm
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    # in a min-heap, the keys of parent nodes are less than or equal to those
    # of the children and the lowest key is in the root node
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []


    def empty(self):
        return len(self.elements) == 0


    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))


    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]


def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10.0 else 0


def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]


def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value


def successors(node):
    successors = []
    # Naar oost
    if node[0] < cf.SIZE -1 and get_grid_value((node[0] + 1, node[1])) != 'b':
        successors.append((node[0] + 1, node[1]))
    # Naar west
    if node[0] > 0 and get_grid_value((node[0] - 1, node[1])) != 'b':
        successors.append((node[0] - 1, node[1]))
    # Naar zuid
    if node[1] < cf.SIZE -1 and get_grid_value((node[0], node[1] + 1)) != 'b':
        successors.append((node[0], node[1] + 1))
    # Naar noord
    if node[1] > 0 and get_grid_value((node[0], node[1] - 1)) != 'b':
        successors.append((node[0], node[1] - 1))


    return successors


class Node:
    def __init__(self, coords, heuristic, parent=None):
        self.coords = coords
        self.parent = parent
        self.current_cost = 0
        self.heuristic = heuristic


def decide_priority(s_node):
    return cf.SIZE - s_node[0] + cf.SIZE - s_node[1]


def search(app, start, goal):
    frontier = PriorityQueue()
    parent_node = Node((0,0), cf.SIZE + cf.SIZE, parent=None)
    frontier.put(item=parent_node, priority=cf.SIZE+cf.SIZE)
    visited = set()
    path = []

    while not frontier.empty():
        s = frontier.get()
        if not s.coords == (0,0): # start node
            parent_node = Node(s.coords, decide_priority(s.coords), parent_node)
        print(s.coords)
        print('{}, {} '.format(cf.SIZE -1,cf.SIZE -1))
        if s.coords == (cf.SIZE -1, cf.SIZE -1):
            current_node = s
            while current_node is not None:
                path.append(current_node.coords)
                current_node = current_node.parent
            path[::-1]
            frontier.elements = []
        else:
            visited.add(s.coords)
            app.plot_node(s.coords, 'pink')
            for successor in successors(s.coords):
                if successor not in visited:
                    successor_node = Node(successor, decide_priority(successor), parent_node)
                    successor_node.current_cost = successor_node.parent.current_cost + 1
                    frontier.put(successor_node, successor_node.current_cost + successor_node.heuristic)
                    app.plot_node(successor, cf.PATH_C)
                    # app.plot_line_segment(s[0], s[1], successor[0], successor[1], color=cf.FINAL_C)
                    app.pause()

    for x in range(len(path)):
        x = x + 1
        app.plot_line_segment(path[x - 1][0], path[x - 1][1], path[x][0], path[x][1], color=cf.FINAL_C)

    # plot a sample path for demonstration
    # for i in range(cf.SIZE-1):
    #     #app.plot_line_segment(i, i, i, i-1, color=cf.PATH_C)
    #     #app.plot_line_segment(i, i, i, i+2, color=cf.PATH_C)
    #     #app.plot_line_segment(i, i, i, i+1, color=cf.FINAL_C)
    #     app.plot_line_segment(i, i+1, i+1, i+1, color=cf.FINAL_C)
    #     app.pause()
