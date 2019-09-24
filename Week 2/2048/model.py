import random
import itertools
import math

MAX_DEPTH = 5

def merge_left(b):
    # merge the board left
    # this is the funcyoin that is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def merge(row, acc):
        # recursive helper for merge_left

        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accumulator
        if len(row) == 1:
            return acc + [x]

        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accumulator, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accumulator, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[0, 0, 0, 2], [0, 0, 2, 4], [0, 0, 8, 2], [4, 8, 4, 2]]
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]


# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                if x == y or x == 0 or y == 0:
                    return True
        return False

    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge function an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, rows):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue

def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [(2, 4, 8, 4), (0, 2, 2, 8), (0, 0, 0, 4), (0, 0, 0, 2)]
    assert merge_down(b) == [(0, 0, 0, 4), (0, 0, 0, 8), (0, 2, 8, 4), (2, 4, 2, 2)]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [(2, 8, 4, 0), (16, 0, 2, 0), (4, 0, 0, 0), (0, 0, 0, 0)]
    assert (merge_down(b)) == [(0, 0, 0, 0), (2, 0, 0, 0), (16, 0, 4, 0), (4, 8, 2, 0)]
    assert (move_exists(b)) == True
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    g = Game()
    for i in range(11):
        g.add_two_four(b)

def get_random_move(board):
    return random.choice(list(MERGE_FUNCTIONS.keys()))

def get_expectimax_move(board):
    best_value = -9999
    best_move = random.choice(list(MERGE_FUNCTIONS.keys()))
    for move in list(MERGE_FUNCTIONS.keys()):
        new_board = MERGE_FUNCTIONS[move](board)
        if new_board != board:
            expectimax_value = search(new_board, MAX_DEPTH, False)

            if expectimax_value > best_value:
                best_value = expectimax_value
                best_move = move

        # print(best_value)
        # print(best_move)
    print('My move is: {}'.format(best_move))
    print('expectimax value: {}'.format(expectimax_value))
    return best_move

def expectimax(board, depth):
    if game_state(board) == 'win' or depth == 0:
        return heuristic_value(board)

    best_value = -9999
    for move in list(MERGE_FUNCTIONS.keys()):
        new_board = MERGE_FUNCTIONS[move](board)
        exp_value = expected_value(exp_successors(new_board))
        value = expectimax(new_board, depth - 1)
        best_value = max(best_value, value)

    return best_value

def search(board, depth, move):
    if game_state(board) == 'win' or depth == 0:
        return heuristic_value(board)

    if move:
        a = -9999
        for m in list(MERGE_FUNCTIONS.keys()):
            new_board = MERGE_FUNCTIONS[m](board)
            a = max(a, search(new_board, depth -1, False))
    else:
        a = 0
        successors_2, successors_4 = exp_successors(board)
        successors = successors_2 + successors_4
        for s in successors:
            if s in successors_2:
                a = a + (0.9 * search(s, depth -1, True)) / len(successors)
            else:
                a = a + (0.1 * search(s, depth -1, True)) / len(successors)

    return a

def expected_value(exp_boards):
    exp_value = 0
    for s in exp_boards:
        exp_value += heuristic_value(s)
    exp_value = exp_value / len(exp_boards)
    return exp_value

def exp_successors(board):
    successors_2 = []
    successors_4 = []
    for x in range(4):
        for y in range(4):
            new_board = list(board)
            if new_board[x][y] == 0:
                new_board[x][y] = 2
                successors_2.append(new_board)
                new_board[x][y] = 4
                successors_4.append(new_board)
    return successors_2, successors_4

def heuristic_value(board):
    value = 0
    if game_state(board) == 'win':
        value += 10000
    last_number = board[0][0]
    for x in range(1, 4):
        if board[x][0] < last_number:
            value += 20
        last_number = board[x][0]

    if board[3][0] > board[3][1]:
        value += 15

    last_number = board[3][1]
    for x in range(2, -1, -1):
        if board[x][1] < last_number:
            value += 10
        last_number = board[x][1]

    highest_number = 0
    for x in range(4):
        for y in range(4):
            if x - 1 >= 0:
                if board[x-1][y] == board[x][y]:
                    value += 10
            if y - 1 >= 0:
                if board[x][y-1] == board[x][y]:
                    value += 10
            if x + 1 <= 3:
                if board[x+1][y] == board[x][y]:
                    value += 10
            if y + 1 <= 3:
                if board[x][y+1] == board[x][y]:
                    value += 10
            if board[x][y] > highest_number:
                highest_number = board[x][y]

    if board[0][0] == highest_number:
        value += 100

    if board[3][3] == 0:
        value += 10

    if board[0][0] == 0 or board[0][0] < highest_number:
        value -= 100

    return value
