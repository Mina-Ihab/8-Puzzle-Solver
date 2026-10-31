import heapq
from itertools import count
from utilities.Class.State import State
from utilities.help import get_legal_moves, goal_test

def a_star_search(initial_state: State, heuristic_function):
    if not isinstance(initial_state, State):
        raise ValueError("This is not an appropriate state.")

    frontier = []
    frontier_states = {}
    visited = set()

    initial_board = initial_state.board
    visited.add(tuple(initial_board.flatten()))

    counter = count()
    estimated_cost = initial_state.depth + heuristic_function(initial_board)

    heapq.heappush(frontier, (estimated_cost, next(counter), initial_state))
    frontier_states[tuple(initial_board.flatten())] = estimated_cost

    expanded = 0
    search_depth = 0
    while len(frontier) != 0:
        _, _, state = heapq.heappop(frontier)
        state_board = state.board

        visited.add(tuple(state_board.flatten()))

        expanded += 1
        search_depth = max(search_depth, state.depth)

        if goal_test(state_board):
            return state, expanded, search_depth

        legal_moves = get_legal_moves(state_board)

        for legal_move in legal_moves:
            child_state = State(legal_move, state.depth + 1)
            estimated_cost = child_state.depth + heuristic_function(legal_move)

            if tuple(legal_move.flatten()) in visited:
                continue

            if tuple(legal_move.flatten()) not in frontier_states or frontier_states[tuple(legal_move.flatten())] > estimated_cost:
                state.add_child(child_state)
                heapq.heappush(frontier, (estimated_cost, next(counter), child_state))
                frontier_states[tuple(legal_move.flatten())] = estimated_cost

    raise ValueError("Can not find a solution.")