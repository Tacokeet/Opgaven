"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a 100-element list, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece.
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`. This is because size of square is 10x10,
   and mn means m*10 + n. This avoids conversion between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""

import random
import time

# The outside edge is marked ?, empty squares are ., black is @, and white is o.
# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}
DEPTH = 6
# Variable show_thought shows more debugging information
SHOW_THOUGHT = False

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11

# 8 directions; note UP_LEFT = -11, we can repeat this from row to row
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    # list all the valid squares on the board.
    # returns a list [11, 12, 13, 14, 15, 16, 17, 18, 21, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves.
# A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()

def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with `square` for `player` in the given
    # `direction`
    # returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be is an occupied line in some direction
    # any(iterable) : Return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)

# Making moves
# When the player makes a move, we need to update the board and flip all the
# bracketed pieces.

def make_move(move, player, board):
    # update the board to reflect the move by the specified player
    # assuming now that the move is valid
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

def legal_moves(player, board):
    # get a list of all legal moves for player
    # legals means : move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())

def game_finished(board):
    if EMPTY not in board:
        return True
    if not any_legal_move(BLACK, board) and not any_legal_move(WHITE, board):
        return True
    return False
# Putting it all together

# Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.
HUMAN = 'human'
AI = 'ai'

def play(black_strategy, white_strategy):
    # play" a game of Othello and return the final board and score
    print('play')
    game_finished_flag = False
    player = BLACK
    board = initial_board()
    while not game_finished_flag:
        print(print_board(board))
        if game_finished(board):
            game_finished_flag = True
            score_player = score(player, board)
            score_opp_player = score(opponent(player), board)
            score_black = score_player if player == BLACK else score_opp_player
            score_white = score_player if player == WHITE else score_opp_player
            determine_winner(score_black, score_white)
            continue
        if player == BLACK:
            move = get_move(BLACK_STRATEGY, player, list(board))
            if not move:
                continue
            if move == 'no_moves':
                print('No moves possible, passing')
                player = opponent(player)
                continue
            board = make_move(move, player, board)
            player = opponent(player)
        else:
            move = get_move(WHITE_STRATEGY, player, list(board))
            if not move:
                continue
            if move == 'no_moves':
                print('No moves possible, passing')
                player = opponent(player)
                continue
            board = make_move(move, player, board)
            player = opponent(player)

def next_player(board, prev_player):
    # which player should move next? Returns None if no legal moves exist
    print('next_player')

def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    print('get_move')
    if strategy == HUMAN:
        return human_move(player, board)
    else:
        return ai_move(player, board)

def score(player, board):
    # compute player's score (number of player's pieces minus opponent's)
    score = 0
    for piece in board:
        if piece == player:
            score += 1
    return score

def determine_winner(score_black, score_white):
    if score_black > score_white:
        print('Black won with {} points more!'.format(score_black - score_white))
    else:
        print('White won with {} points more!'.format(score_white - score_black))

def human_move(player, board):
    # If there are no legal moves, pass turn
    if not any_legal_move(player, board):
        return 'no_moves'
    # Let the player decide what move to do
    print('What move will you do? Choose from: ')
    print(legal_moves(player, board))
    move = input()
    valid = is_valid(move)
    # Check if the move is valid and possible
    if not valid:
        print('This move is not on the board or you typed something wrong')
        return False
    legal = is_legal(move, player, board)
    if move not in legal_moves(player, board):
        print('This is not a legal move, try something else')
        return False
    return move

def ai_move(player, board):
    print('Hello, im ai')
    start_turn_time = time.time()
    # If there are no legal moves, pass turn
    if not any_legal_move(player, board):
        return 'no_moves'

    moves = legal_moves(player, board)
    best_value = -9999
    best_move = moves[random.randrange(len(moves))]
    # For all next moves this player can do,
    # negamax those moves to get the best move
    for move in moves:
        # Possible next state
        new_board = make_move(move, player, list(board))

        # Negamax from this state and its value
        negamax_value = -1 * negamax(new_board, -9999, 9999, -1, opponent(player), DEPTH)
        # If this value is better than what we had, we use the new value and move

        if negamax_value > best_value:
            best_value = negamax_value
            best_move = move
        # Debugging information
        if SHOW_THOUGHT:
            print(print_board(new_board))
            print('------------')
            print('nm value: {}'.format(negamax_value))
            print(best_value)
            print('Best move: {}'.format(best_move))

    # Print some information as move and time
    print('My move is: {}'.format(best_move))
    after_turn_time = time.time()
    timing = after_turn_time - start_turn_time
    color = ''
    if timing < 1.0:
        color = '\033[92m'
    elif timing < 3.0:
        color = '\033[93m'
    else:
        color = '\033[91m'
    print('Ended turn in: {} {} \033[0m'.format(color, timing))

    return best_move

# Negamax algoritme
def negamax(board, a, b, player_value, player, depth):
    # Als het bord geen lege velden meer heeft, is het een end-state
    if EMPTY not in board or depth == 0:
        # Determine the heuristic value of this end state
        return get_heuristic_value(player, board, player_value)

    best_value = -9999
    for move in legal_moves(player, board):
        # Maak voor de mogelijke move een nieuw bord, de volgende state
        new_board = make_move(move, player, list(board))
        value = -1 * negamax(new_board, -b, -a, -1 * player_value, opponent(player), depth - 1)
        best_value = max(best_value, value)
        # Pruning
        a = max(a, best_value)
        if a >= b:
            # print("alpha {} >= beta {}".format(a, b))
            break
    return best_value

def get_heuristic_value(player, board, player_value):
    end_value = 0

    # upper row
    for x in range(11, 18):
        if board[x] == player:
            end_value += 1
    # bottom row
    for x in range(81, 88):
        if board[x] == player:
            end_value += 1
    # left row + double corner
    for x in range(11, 81, 10):
        if board[x] == player:
            end_value += 1
    # right row + double corner
    for x in range(18, 88, 10):
        if board[x] == player:
            end_value += 1
    end_value += player_value * score(player, board)

    return end_value


def simple_ai(player, board):
    moves = legal_moves(player, board)
    return moves[random.randrange(len(moves))]

black_typing_correct = False
while not black_typing_correct:
    print('Who plays black? -ai- or -human-')
    BLACK_STRATEGY = raw_input()
    if BLACK_STRATEGY == 'human' or BLACK_STRATEGY == 'ai':
        black_typing_correct = True
    else:
        print('Something didn\'t match, please review your typing')

white_typing_correct = False
while not white_typing_correct:
    print('Who plays white? -ai- or -human-')
    WHITE_STRATEGY = raw_input()
    if WHITE_STRATEGY == 'human' or WHITE_STRATEGY == 'ai':
        white_typing_correct = True
    else:
        print('Something didn\'t match, please review your typing')

play(BLACK_STRATEGY, WHITE_STRATEGY)
# Play strategies
