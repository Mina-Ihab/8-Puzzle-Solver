from utilities.help import build_path
from PySide6.QtCore import QThread, Signal

class RunSearch(QThread):
    solved = Signal(object, int, int)
    failed = Signal(str)

    def __init__(self, search_function, initial_state):
        super().__init__()
        self.search_function = search_function
        self.initial_state = initial_state

    def run(self):
        try:
            end_state, expansion_count, search_depth = self.search_function(self.initial_state)
            path = build_path(end_state)
        except ValueError as er:
            self.failed.emit(f"Search Failed: {er}")
            return
        self.solved.emit(path, expansion_count, search_depth)