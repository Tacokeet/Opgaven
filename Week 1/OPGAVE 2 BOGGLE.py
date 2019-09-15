# Variables
board = [['P', 'I', 'E', 'T'], ['G', 'A', 'A', 'T'], ['A', 'T', 'M', 'S'], ['H', 'U', 'I', 'S']]
prefixes = []
neighbours = [(0, -1), (-1, 0), (1, 0), (0, 1)]
file = open('words.txt', 'r')
words = [line.split() for line in file.readlines()]

# Create prefixed list
for word in words:
    for number in range(len(word[0])):
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
        # changed the coordinates to it can loop around the board
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
    return list(set(found_words))


def solve():
    result = []
    # get the coordinates of the board
    for x in range(len(board)):
        for y in range(len(board)):
            result += find(x, y, board[x][y], {(x, y)})
    return set(result)


print((solve()))
