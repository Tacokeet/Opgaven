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


def nearest(city, cities):
    dis = {}
    for x in cities:
        dis[distance(city, x)] = x
        sorted_dict = collections.OrderedDict(sorted(dis.items()))
        # print(sorted_dict)
    return sorted_dict


def checkCross(city, visited):
    for x in range(len(visited) - 1):
        # print(city)
        if check_intersect(visited[x], visited[x + 1], visited[len(visited) - 1], city):
            return True
    return False


def paththing(nextCity, visited, cities):
    # print(nextCity)
    # print(cities)

    # print(visited)
    path = []
    if len(cities) is len(visited):
        if check_intersect(visited[len(visited) - 2], visited[len(visited) - 1], nextCity, visited[0]):
            print("")
        else:
            path.append(nextCity)
            path.append(visited[0])

    if checkCross(nextCity, visited):
        return path
    path.append(nextCity)
    # cities.remove(nextCity)

    # print(nearest(nextCity, cities).items())
    for x in nearest(nextCity, cities).items():
        # print(x[1])
        if x[1] not in visited:
            visited.append(x[1])
            cities.remove(x[1])
            path.extend(paththing(x[1], visited, cities))
            visited.remove(x[1])
            cities.append(x[1])
            print(path)
            print(len(path))
            print('----------------------------------------------------------------------------------------------------------------------------')

    return path


def nearest_neighbour(cities):
    cities = list(cities)
    visited = []
    dis = {}
    start = cities[random.randrange(len(cities))]
    visited.append(start)
    cities.remove(start)
    while len(cities) is not 0:
        for x in cities:
            dis[distance(visited[len(visited) - 1], x)] = x
        # if len(visited) > 2:
        #
        # print(dis)
        visited.append(dis[min(dis.keys())])
        cities.remove(dis[min(dis.keys())])
        # print(cities)
        sorted_dict = collections.OrderedDict(sorted(dis.items()))
        print(sorted_dict)
        dis.clear()

    # print(visited)
    # print(len(visited))
    # print(check_intersect(visited[9], visited[0], visited[5], visited[6]))
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


# plot_tsp(nearest_neighbour, make_cities(10))


def go(cities):
    cities = list(cities)
    start = cities[random.randrange(len(cities))]
    return paththing(start, [start], cities)


print(go(make_cities(10)))
