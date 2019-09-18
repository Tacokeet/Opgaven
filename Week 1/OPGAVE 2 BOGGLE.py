import time
import string
import random

# Start the timer to setup board
before_words_time = time.time()
print('\033[95mGoing through words... \033[0m')

# Variables
# board = [['P', 'I', 'E', 'T', 'A'], ['G', 'A', 'A', 'T', 'E'], ['A', 'T', 'M', 'S', 'F'], ['H', 'U', 'I', 'S', 'A']]
prefixes = []
neighbours = [(0, -1), (-1, 0), (1, 0), (0, 1)]
file = open('words.txt', 'r')
words = [line.split() for line in file.readlines()]
seen_prefixes = set(prefixes)
n = 4
board = []
for x in range(n):
    board.append([random.choice(string.ascii_letters)])
    for y in range(n-1):
        board[x].append(random.choice(string.ascii_letters))

# Stop the timer
after_words_time = time.time()
print('Done preparing in: ')
print(after_words_time - before_words_time)

# Start the timer for doing the job
before_time = time.time()
print('\033[95mLooking for words in the board...\033[0m')

# Create prefixed list
for word in words:
    for number in range(len(word[0])):
        if word[0][0:number] not in seen_prefixes:
            seen_prefixes.add(word[0][0:number])
            prefixes.append(word[0][0:number])


# find all possible words
def find(gx, gy, position, traveled):
    found_words = []
    if [position.lower()] in words:
        found_words.append(position)
    if position.lower() not in prefixes:
        return found_words
    for bx, by in neighbours:
        rx, ry = gx + bx, gy + by
        # changed the coordinates so it can loop around the board
        if rx < 0:
            rx = len(board) - 1
        if ry < 0:
            ry = len(board) - 1
        if rx > len(board) - 1:
            rx = 0
        if ry > len(board) - 1:
            ry = 0
        if (rx, ry) not in traveled:
            traveled.add((rx, ry))
            # give the  neighbour letter to the function and repeat!
            found_words.extend(find(rx, ry, position + board[rx][ry], traveled))
            traveled.remove((rx, ry))
    return found_words


def solve():
    result = []
    # get the coordinates of the board
    for x in range(len(board)):
        for y in range(len(board)):
            # find all words for coordinates 0,0 | 0,1 | ...
            # print(x, y)
            result += find(x, y, board[x][y], {(x, y)})
    return result


print(solve())

# Stop the timer
after_time = time.time()
print('Done looking in: \033[92m {} \033[0m'.format(after_time - before_time))
