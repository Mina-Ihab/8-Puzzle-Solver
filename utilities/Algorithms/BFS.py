import queue
from utilities.Class.State import State
from utilities.help import get_legal_moves, goal_test

def bfs_search(initial_state: State):
    if not isinstance(initial_state, State):
        raise ValueError("This is not an appropriate state.")

    frontier = queue.Queue()
    visited_set = set()
    frontier_set = set()

    initial_board = initial_state.board
    frontier_set.add(tuple(initial_board.flatten()))
    frontier.put(initial_state)

    expanded = 0
    search_depth = 0
    while not frontier.empty():
        state = frontier.get()
        state_board = state.board

        frontier_set.remove(tuple(state_board.flatten()))
        visited_set.add(tuple(state_board.flatten()))

        expanded += 1
        search_depth = max(search_depth, state.depth)

        if goal_test(state_board):
            return state, expanded, search_depth

        legal_moves = get_legal_moves(state_board)

        for legal_move in legal_moves:
            child_tuple = tuple(legal_move.flatten())

            if child_tuple not in frontier_set and child_tuple not in visited_set:
                child_state = State(legal_move, depth=state.depth + 1)
                state.add_child(child_state)

                frontier.put(child_state)
                frontier_set.add(child_tuple)

    raise ValueError("Can not find a solution.")
