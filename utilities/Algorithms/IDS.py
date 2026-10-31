import queue
from utilities.Class.State import State
from utilities.help import get_legal_moves, goal_test

NOT_FOUND = -1

def dls_search(initial_state: State, limit: int):
    if not isinstance(initial_state, State):
        raise ValueError("This is not an appropriate state.")

    frontier = queue.LifoQueue()
    visited_set = {}

    initial_board = initial_state.board
    visited_set[tuple(initial_board.flatten())] = initial_state.depth

    frontier.put(initial_state)

    expanded = 0
    while not frontier.empty():
        state = frontier.get()
        state_board = state.board

        expanded += 1

        if goal_test(state_board):
            return state, expanded

        if state.depth >= limit:
            continue

        legal_moves = get_legal_moves(state_board)

        child_depth = state.depth + 1

        for legal_move in legal_moves:
            child_tuple = tuple(legal_move.flatten())

            if child_tuple not in visited_set or visited_set[child_tuple] > child_depth:
                child_state = State(legal_move, child_depth)
                state.add_child(child_state)

                frontier.put(child_state)
                visited_set[child_tuple] = child_depth

    return NOT_FOUND, expanded

def ids_search(initial_state: State):

    limit = 0

    while True:

        first_state = State(initial_state.board, depth=0)
        state, expanded = dls_search(first_state, limit)

        if state is NOT_FOUND:
            limit += 1
            continue

        break

    return state, expanded, limit

