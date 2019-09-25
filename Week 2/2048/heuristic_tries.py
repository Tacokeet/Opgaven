def heuristic_v1(board):
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


    if board[0][0] == highest_number:
        value += 100

    if board[3][3] == 0:
        value += 10

    if board[0][0] == 0 or board[0][0] < highest_number:
        value -= 100

    return value
