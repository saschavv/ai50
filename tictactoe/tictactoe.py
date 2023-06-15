"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], 
            [EMPTY, EMPTY, EMPTY], 
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_moves = 0
    o_moves = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == X:
                x_moves += 1
            elif board[i][j] == O:
                o_moves += 1
    if x_moves <= o_moves:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = []

    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                result.append((i, j))

    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]

    if board[i][j] != EMPTY:
        raise Exception("Invalid action, postion already taken")

    local_board = copy.deepcopy(board)
    current_player = player(board)
    local_board[i][j] = current_player

    return local_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # row winner
    for i in range(0, 3):
        if board[i][1] == board[i][0] and board[i][2] == board[i][0]:
            return board[i][0]
    # column winner
    for j in range(0, 3):
        if board[1][j] == board[0][j] and board[2][j] == board[0][j]:
            return board[0][j]
    # orthogonal
    if board[1][1] == board[0][0] and board[2][2] == board[0][0]:
        return board[0][0]
    if board[1][1] == board[0][2] and board[2][0] == board[0][2]:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def max_value(board):
    if terminal(board):
        return utility(board), None
    v = -math.inf
    a = None
    for action in actions(board):
        local_v = min_value(result(board, action))[0]
        if local_v > v:
            v = local_v
            a = action
    return v,a


def min_value(board):
    if terminal(board):
        return utility(board), None
    v = math.inf
    a = None
    for action in actions(board):
        local_v = max_value(result(board, action))[0]
        if local_v < v:
            v = local_v
            a = action
    return v,a


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]
        