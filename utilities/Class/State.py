import numpy as np

class State:
    def __init__(self, board: np.ndarray, depth: int):
        self.board = board
        self.parent = None
        self.children = []
        self.depth = depth

    def add_child(self, child: State):
        if not isinstance(child, State):
            raise ValueError("This is not a state.")

        self.children.append(child)
        child.parent = self


