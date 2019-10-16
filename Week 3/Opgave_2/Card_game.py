from itertools import permutations
from copy import deepcopy


def pb(b):
    print "\n\
. . {} .\n\
{} {} {} .\n\
. {} {} {}\n\
. . {} .".format(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7])

cards = ['A', 'A', 'H', 'H', 'D', 'D', 'B', 'B']
board = {
    0: '',
    1: '',
    2: '',
    3: '',
    4: '',
    5: '',
    6: '',
    7: '',
}
dfs_count = [0]
all_neighbours = [[0, 3], [1, 2], [2, 3], [2, 4], [3, 5], [4, 5], [5, 6], [5, 7]]
# print list(permutations('AAHHDDBB',7))
spots = (0, 1, 2, 3, 4, 5, 6, 7)

#   - - 0 -
#   1 2 3 -
#   - 4 5 6
#   - - 7 -
#
print("Aantal permutaties: {}".format(len(set(permutations(cards)))))

def brute_force(board):
    count_permutations = 0
    for spots in set(permutations(cards)):
        count_permutations += 1
        # Aanmaken van het bord
        for x in range(8):
            board[x] = spots[x]

        if already_a_complete_fucking_failure(board):
            continue
        print("Brute Force")
        print("Aantal iteraties: {}".format(count_permutations))
        pb(board)
        break

def x_has_y(x, y, i, b):
    # Gegeven een positie i, en units X en Y,
    # Kijk of 1 van de neighbours van unit X op i een Y is.
    x_has_y = False

    neighbours_of_X = []
    # Loop over neighbours, put in neighbours_of_X
    for neighbours in all_neighbours:
        if i in neighbours:
            neighbours_of_X.append(neighbours)
    for neighbour_of_X in neighbours_of_X:
        # Kijk alleen naar het onderdeel van neighbours lijst welke niet i is.
        if neighbour_of_X[0] == i:
            if (b[neighbour_of_X[1]] == y) or (b[neighbour_of_X[1]] == ''):
                x_has_y = True
        else:
            if (b[neighbour_of_X[0]] == y) or (b[neighbour_of_X[0]] == ''):
                x_has_y = True
    return x_has_y

def goed(board):
    # Als bord niet empty is en niet een failure, dan is het goed
    # Dit is de win-condition
    for spot in board.values():
        if spot == '':
            return False
    return not already_a_complete_fucking_failure(board)

def already_a_complete_fucking_failure(board):
    # True = yes it IS a fucking failure
    for neighbours in all_neighbours:
        # Kijk of A naast D ligt
        if board[neighbours[0]] == 'A' and board[neighbours[1]] == 'D':
            return True
        if board[neighbours[1]] == 'A' and board[neighbours[0]] == 'D':
            return True
        if (board[neighbours[0]] == board[neighbours[1]]) and board[neighbours[0]] != '':
            return True
    # Loop over units of empty spaces in geval van DFS
    for i in range(len(board)):
        unit = board[i]
        if unit == '':
            continue
        elif unit == 'A':
            if not x_has_y('A', 'H', i, board):
                return True
        elif unit == 'H':
            if not x_has_y('H', 'D', i, board):
                return True
        elif unit == 'D':
            if not x_has_y('D', 'B', i, board):
                return True
    return False

def successors(board):
    cards = ['A', 'A', 'H', 'H', 'D', 'D', 'B', 'B']
    options = []
    empty = True
    for spot in board.values():
        if spot != '':
            empty = False
        if spot in cards:
            cards.remove(spot)

    # is board empty?
    if empty:
        cards = ['A', 'H', 'B', 'D']
        for c in cards:
            board_copy = deepcopy(board)
            board_copy[0] = c
            options.append(board_copy)
        return options

    for neighbour_list in all_neighbours:
        if board[neighbour_list[0]] == '' and board[neighbour_list[1]] != '':
            empty = 0
            unit = 1
        elif board[neighbour_list[1]] == '' and board[neighbour_list[0]] != '':
            empty = 1
            unit = 0
        else:
            continue
        for card in cards:
            # This is where we can use arc_consistency to determine actual valid options
            if card != neighbour_list[unit]:
                board_copy = deepcopy(board)
                board_copy[neighbour_list[empty]] = card
                if board_copy not in options:
                    options.append(board_copy)
    return options


def dfs(board, visited):
    visited.append(board)
    dfs_count[0] += 1
    if goed(board):
        print("DFS")
        print("Aantal iteraties: {}".format(dfs_count[0]))
        pb(board)
        return board

    # Go backtrack or no?
    if already_a_complete_fucking_failure(board):
        return False

    # Go forward!
    result = None
    for successor in successors(board):
        if successor in visited:
            continue
        result = dfs(successor, visited)
        # If a successor return false, it backtracked to this point
        if result != False:
            break
    if result == None:
        return False
    return result

print("_____________________________")
result = dfs(deepcopy(board), [])
print("_____________________________")
print(brute_force(board))
