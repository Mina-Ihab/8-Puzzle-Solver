import numpy as np
from math import sqrt
from utilities.Class.State import State

UP = -1
DOWN = 1
RIGHT = 1
LEFT = -1

SIZE = 3
GOAL_BOARD = np.array([
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
])

def get_legal_moves(board: np.ndarray):
    z_r, z_c = find_blank(board)

    copy = board.copy()
    legal_moves = []

    if z_r + UP >= 0:
        copy[z_r][z_c], copy[z_r+UP][z_c] = copy[z_r+UP][z_c], copy[z_r][z_c]
        legal_moves.append(copy)

    copy = board.copy()

    if z_r + DOWN < SIZE:
        copy[z_r][z_c], copy[z_r + DOWN][z_c] = copy[z_r + DOWN][z_c], copy[z_r][z_c]
        legal_moves.append(copy)

    copy = board.copy()

    if z_c + RIGHT < SIZE:
        copy[z_r][z_c], copy[z_r][z_c + RIGHT] = copy[z_r][z_c + RIGHT], copy[z_r][z_c]
        legal_moves.append(copy)

    copy = board.copy()

    if z_c + LEFT >= 0:
        copy[z_r][z_c], copy[z_r][z_c + LEFT] = copy[z_r][z_c + LEFT], copy[z_r][z_c]
        legal_moves.append(copy)

    return legal_moves

def find_blank(board: np.ndarray):
    return np.argwhere(board == 0).flatten()

def manhattan_distance(board: np.ndarray):
    total_manhattan = 0
    for r in range(SIZE):
        for c in range(SIZE):
            num = board[r][c]

            if num == 0:
                continue

            x, y = np.argwhere(GOAL_BOARD == num).flatten()

            total_manhattan += (abs(x - r) + abs(y - c))

    return total_manhattan

def euclidean_distance(board: np.ndarray):
    total_euclidean = 0
    for r in range(SIZE):
        for c in range(SIZE):
            num = board[r][c]

            if num == 0:
                continue

            x, y = np.argwhere(GOAL_BOARD == num).flatten()

            total_euclidean += sqrt((r - x)**2 + (c - y)**2)

    return total_euclidean

def goal_test(board: np.ndarray):
    return np.array_equal(board, GOAL_BOARD)

def build_path(end_state: State):
    current_state = end_state
    r_path = []

    while current_state is not None:
        r_path.append(current_state)
        current_state = current_state.parent

    return r_path[::-1]

def get_inversion(initial_board: np.ndarray):
    inversions = 0

    flatten_board = initial_board.flatten()

    for i in range(SIZE * SIZE):
        temp = flatten_board[i]

        if temp == 0:
            continue

        for j in range(i+1, SIZE * SIZE):

            if flatten_board[j] == 0:
                continue

            if temp > flatten_board[j]:
                inversions += 1

    return inversions

def is_solvable(initial_board: np.ndarray):
    inversions = get_inversion(initial_board)
    return inversions % 2 == 0
