from copy import deepcopy
import string
import random
import time

empty_oever = set()
state = ({"F", "C", "G", "W"}, empty_oever)

# n = 100
#
# for x in range(n - 4):
#     state[0].add(random.choice(string.ascii_letters).upper())

def check_if_valid(state_to_check):
    # print("Validating..")
    if len(state_to_check[0]) < 3: # The left oever only has 2 objects left
        if "C" in state_to_check[0] and "G" in state_to_check[0]:
            # print('The Goat ate the Cabbage!')
            return False
        if "G" in state_to_check[0] and "W" in state_to_check[0]:
            # print('The Wolf ate the Goat!')
            return False
    if len(state_to_check[1]) < 3: # The right oever only has 2 objects left
        if "C" in state_to_check[1] and "G" in state_to_check[1]:
            # print('The Goat ate the Cabbage!')
            return False
        if "G" in state_to_check[1] and "W" in state_to_check[1]:
            # print('The Wolf ate the Goat!')
            return False
    # print('valid')
    return state_to_check

def successors(node):
    prev_state = deepcopy(node)

    possible_successors = []
    good_successors = []

    move = "left" if "F" in prev_state[1] else "right"

    if move == "left":
        prev_state[1].remove("F")
        prev_state[0].add("F")
        new_state = deepcopy(prev_state)
        possible_successors.append(deepcopy(new_state))

        for animal_or_cabbage in prev_state[1]:
            new_state = deepcopy(prev_state)
            new_state[1].remove(animal_or_cabbage)
            new_state[0].add(animal_or_cabbage)
            possible_successors.append(deepcopy(new_state))
    elif move == "right":
        prev_state[0].remove("F")
        prev_state[1].add("F")
        new_state = deepcopy(prev_state)
        possible_successors.append(deepcopy(new_state))

        for animal_or_cabbage in prev_state[0]:
            new_state = deepcopy(prev_state)
            new_state[0].remove(animal_or_cabbage)
            new_state[1].add(animal_or_cabbage)
            possible_successors.append(deepcopy(new_state))

    for successor in possible_successors:
        if check_if_valid(successor):
            good_successors.append(check_if_valid(successor))

    return good_successors

visited = []
path = []
def dfs(node, visited, path):
    path.append(node)                             # 1
    if len(node[0]) == 0:                         # 1
        return True

    visited.append(node)                          #
    for child in successors(node):                # How many in successors
        if child not in visited:                  # How many in visited
            if dfs(child, visited, path):
                return True
    path.pop()
    return False
before_time = time.time()
print('\033[95mGoing...\033[0m')
dfs(state, visited, path)

prev_p = False
for p in path:
    if prev_p:
        left_or_right = 0 if "F" in p[0] else 1
        format = '<-- {} --<' if left_or_right == 0 else '>-- {} -->'
        print(format.format(' '.join(p[left_or_right] - prev_p[left_or_right])))
        prev_p = p
    if not prev_p:
        prev_p = p
    print(''.join(p[0]) + '|'+ ''.join(p[1]))

after_time = time.time()
print('Done in: \033[92m {} \033[0m'.format(after_time - before_time))
