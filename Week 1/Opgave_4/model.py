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
    # Naar zuid
    if node[1] < cf.SIZE and get_grid_value((node[0], node[1] + 1)) != 'b':
        successors.append((node[0], node[1] + 1))
    # Naar noord
    if node[1] > 0 and get_grid_value((node[0], node[1] - 1)) != 'b':
        successors.append((node[0], node[1] - 1))
    # Naar oost
    if node[0] < cf.SIZE and get_grid_value((node[0] + 1, node[1])) != 'b':
        successors.append((node[0] + 1, node[1]))
    # Naar west
    if node[0] > 0 and get_grid_value((node[0] - 1, node[1])) != 'b':
        successors.append((node[0] - 1, node[1]))

    return successors

def decide_priority(c_node, s_node):
    p = 10
    pos = c_node[1] - c_node[0]
    # als p groter is dan 0 naar het oosten
    # als p kleiner is dan 0 naar het zuiden
    if s_node[0] > c_node[0]: # we gaan rechts
        if pos == 0:
            p = 5
        elif pos > 5:
            p = 1
        elif pos > 0:
            p = 3
        else:
            p = 4
    if s_node[1] > c_node[1]: # we gaan naar onder
        if pos == 0:
            p = 5
        elif pos < -5:
            p = 1
        elif pos < 0:
            p = 3
        else:
            p = 4
    return (-(s_node[0] - c_node[0]) + (s_node[1] - c_node[1]))

def search(app, start, goal):
    frontier = PriorityQueue()
    frontier.put(item=(0,0), priority=1)
    visited = set()

    # plot a sample path for demonstration
    # for i in range(cf.SIZE-1):
    #     #app.plot_line_segment(i, i, i, i-1, color=cf.PATH_C)
    #     #app.plot_line_segment(i, i, i, i+2, color=cf.PATH_C)
    #     #app.plot_line_segment(i, i, i, i+1, color=cf.FINAL_C)
    #     app.plot_line_segment(i, i+1, i+1, i+1, color=cf.FINAL_C)
    #     app.pause()
    while not frontier.empty():
        s = frontier.get()
        if s == (cf.SIZE, cf.SIZE):
            return
        visited.add(s)
        app.plot_node(s, cf.PATH_C)
        for successor in successors(s):
            if successor not in visited:
                print('------------')
                print(s)
                print(successor)
                print(decide_priority(s, successor))
                frontier.put(successor, decide_priority(s, successor))
                # app.plot_line_segment(s[0], s[1], successor[0], successor[1], color=cf.FINAL_C)
                app.pause()
