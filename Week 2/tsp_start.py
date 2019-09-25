import matplotlib.pyplot as plt
import random
import time
import itertools
import collections
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')


def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)


def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)


def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # cities is a set, sets don't support indexing
    start = next(iter(cities))
    return [[start] + list(rest)
            for rest in itertools.permutations(cities - {start})]


# Start of my own algorithm
def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

    if val == 0:
        return 0
    elif val > 1:
        return 1
    else:
        return 2


def check_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    return False


def nearest(city, cities, start, path, visited):
    dis = {}
    for x in cities:
        dis[distance(city, x)] = x
    dis = collections.OrderedDict(sorted(dis.items()))
    dis[0] = start
    # print(len(dis))
    # print(dis)
    plot_tour(visited)
    return dis


def checkCross(city, visited):
    for x in range(len(visited) - 1):
        if check_intersect(visited[x], visited[x + 1], visited[len(visited) - 1], city):
            return True
    return False


def paththing(nextCity, visited, cities, start):
    # print(nextCity)
    # print(cities)

    # print(visited)
    path = []
    # if len(cities) is len(visited):
    #     if check_intersect(visited[len(visited) - 2], visited[len(visited) - 1], nextCity, visited[0]):
    #         return path
    #     else:
    #         path.append(nextCity)
    #         path.append(visited[0])

    if checkCross(nextCity, visited):
        print('Cros Found!!')
        return path
    path.append(nextCity)
    # print(nearest(nextCity, cities).items())
    for x in nearest(nextCity, cities, start, path, visited).items():
        if len(visited) is 10:
            # print(start)
            # print(x[1])
            if checkCross(x[1], visited):
                print('Cros detected')
                return path
            else:
                print('PERFECT PATH')
                break
        # print(x[1])
        # print(start)
        if x[1] not in visited:
            visited.append(x[1])
            cities.remove(x[1])
            path.extend(paththing(x[1], visited, cities, start))

            visited.remove(x[1])
            cities.append(x[1])
            # print(path)
            # print(len(path))
            # print('----------------------------------------------------------------------------------------------------------------------------')
    return path


# end of my own algorithm

def optSwap(route, i, k):
    new_route = []
    for x in range(i):
        new_route.append(route[x])
    for x in range(k, i - 1, -1):
        new_route.append(route[x])
    for x in range(k + 1, len(route)):
        new_route.append(route[x])
    return new_route


def two_opt(route, start):
    route.append(start)
    # improved = True
    counter = 0
    while counter < 10:
        # improved = False
        best_distance = tour_length(route)
        for i in range(1, len(route) - 2):
            for k in range(i + 1, len(route) - 1):
                new_route = optSwap(route, i, k)
                new_distance = tour_length(new_route)
                if new_distance < best_distance:
                    route = new_route
                    best_distance = new_distance
                    # improved = True
                    counter = 0
                else:
                    counter += 1

    return route


def nearest_neighbour(cities):
    cities = list(cities)
    visited = []
    dis = {}
    start = cities[0]
    visited.append(start)
    cities.remove(start)
    while len(cities) is not 0:
        for x in cities:
            dis[distance(visited[len(visited) - 1], x)] = x
        visited.append(dis[min(dis.keys())])
        cities.remove(dis[min(dis.keys())])
        dis.clear()

    return two_opt(visited, start)


def two_nearest(cities):
    cities = list(cities)
    visited = []
    dis = {}
    start = cities[0]
    visited.append(start)
    cities.remove(start)
    while len(cities) is not 0:
        for x in cities:
            dis[distance(visited[len(visited) - 1], x)] = x
        visited.append(dis[min(dis.keys())])
        cities.remove(dis[min(dis.keys())])
        dis.clear()

    return visited


def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i - 1])
               for i in range(len(tour)))


def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(41)  # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height))
                     for c in range(n))


def plot_tour(tour):
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled')  # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()


def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.time()
    tour = algorithm(cities)
    t1 = time.time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)


plot_tsp(nearest_neighbour, make_cities(100))
plot_tsp(two_nearest, make_cities(100))


def go(cities):
    cities = list(cities)
    start = cities[random.randrange(len(cities))]
    cities.remove(start)
    return paththing(start, [start], cities, start)
