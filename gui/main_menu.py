import time
import numpy as np
from pathlib import Path
from functools import partial
from PySide6.QtGui import QIcon
from gui.run_search import RunSearch
from PySide6.QtCore import Qt, QTimer
from utilities.Class.State import State
from utilities.Algorithms.BFS import bfs_search
from utilities.Algorithms.DFS import dfs_search
from utilities.Algorithms.IDS import ids_search
from utilities.Algorithms.AStar import a_star_search
from utilities.help import is_solvable, manhattan_distance, euclidean_distance
from PySide6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget,
                               QGroupBox, QPushButton, QHBoxLayout, QGridLayout,
                               QLineEdit, QSlider)

ICON_PATH = Path(__file__).resolve().parent / "assets" / "icon.png"

SIZE = 3

WINDOW_WIDTH = 550
WINDOW_HEIGHT = 870

PUZZLE_BOX_SIZE = 350

BOX_WIDTH = 535
BOX_HEIGHT = 115

STATES_HEIGHT = 180

ALGORITHM_HEIGHT = 130

SOLVE_HEIGHT = 50

TILE_SIZE = 100

INTERVAL_MILLISECOND = 100
MAX_DELAY_MILLISECOND = 1000
MIN_DELAY_MILLISECOND = 0

STATUS_STYLES = {
    "error": """
        background-color: #7F1D1D;
        color: #FCA5A5;
        border: 1px solid #EF4444;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
    """,
    "success": """
        background-color: #14532D;
        color: #86EFAC;
        border: 1px solid #22C55E;
        border-radius: 8px;
        font-size: 14px;
        font-weight: bold;
    """,
    "none": """
        background-color: transparent;
    """
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(str(ICON_PATH)))

        self.worker = None

        self.board = np.array([
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ])
        self.tiles = []

        self.algorithms = {
            "BFS": bfs_search,
            "DFS": dfs_search,
            "IDS": ids_search,
            "A* (Manhattan)": partial(a_star_search, heuristic_function=manhattan_distance),
            "A* (Euclidean)": partial(a_star_search, heuristic_function=euclidean_distance),
        }
        self.selected_algorithm = None

        self.path = None
        self.path_index = None
        self.expansion_count = 0
        self.search_depth = 0

        self.setWindowTitle("8-Puzzle Solver")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        main_widget = QWidget()
        main_widget.setStyleSheet("""
            QWidget {
                background-color: #101827;
            }
            
            QPushButton {
                background-color: #334155;
                color: #F1F5F9;
            }

            QPushButton:hover {
                background-color: #38BDF8;
                color: #101827;
            }

            QPushButton:pressed {
                background-color: #0284C7;
                color: #FFFFFF;
            }

            QPushButton:disabled {
                background-color: #1E293B;
                color: #64748B;
            }
            
            QPushButton:checked {
                background-color: #38BDF8;
                color: #101827;
            }
        """)

        self.setCentralWidget(main_widget)

        content_layout = QVBoxLayout(main_widget)

        # Puzzle Panel
        self.puzzle_panel = QGroupBox("Puzzle Panel", main_widget)
        self.puzzle_layout = QGridLayout(self.puzzle_panel)

        self.puzzle_panel.setFixedSize(PUZZLE_BOX_SIZE, PUZZLE_BOX_SIZE)

        self.create_tiles()
        self.update_tiles()

        # Input Panel
        input_panel = QGroupBox("Input Panel", main_widget)
        input_layout = QVBoxLayout(input_panel)

        input_panel.setFixedSize(BOX_WIDTH, BOX_HEIGHT)

        self.system_msg = QLabel(input_panel)
        self.show_status("", "none")

        self.input_line = QLineEdit(input_panel)
        self.input_line.setPlaceholderText("Write the initial state like this (012345678)")
        self.input_line.setStyleSheet("""
            background-color: #334155;
            color: #F1F5F9;
        """)

        self.insert_button = QPushButton(input_panel)
        self.insert_button.setText("Insert")

        self.insert_button.clicked.connect(self.insert_tiles)

        input_layout.addWidget(self.system_msg)
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(self.insert_button)

        # States Panel
        states_panel = QGroupBox("States Panel", main_widget)
        states_layout = QVBoxLayout(states_panel)

        states_panel.setFixedSize(BOX_WIDTH, STATES_HEIGHT)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.start_time = 0.0

        self.timer_label = QLabel(f"Search Time: {self.start_time} ms")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("""
            color: #38BDF8;
            font-size: 16px;
            font-weight: bold;
        """)

        states_layout.addWidget(self.timer_label)

        self.states_label = QLabel("Expanded Nodes: 0 | Path Cost: 0\n Search Depth: 0 | Number of Moves: 0 | Moves Left: 0")

        self.states_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        states_layout.addWidget(self.states_label)

        control_layout = QHBoxLayout()

        self.prev_button = QPushButton("Previous Step")
        self.prev_button.setEnabled(False)
        self.prev_button.clicked.connect(self.prev_move)
        self.auto_button = QPushButton("Auto Solve")
        self.auto_button.setEnabled(False)
        self.auto_button.clicked.connect(self.auto_move)
        self.next_button = QPushButton("Next Step")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.next_move)

        control_layout.addWidget(self.prev_button)
        control_layout.addWidget(self.auto_button)
        control_layout.addWidget(self.next_button)

        states_layout.addLayout(control_layout)

        self.delay = MAX_DELAY_MILLISECOND
        self.speed_label = QLabel("Move Speed = 1.0 second/move")
        self.speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(MIN_DELAY_MILLISECOND, MAX_DELAY_MILLISECOND)
        self.speed_slider.setValue(MAX_DELAY_MILLISECOND)

        self.speed_slider.valueChanged.connect(self.update_speed_label)

        states_layout.addWidget(self.speed_label)
        states_layout.addWidget(self.speed_slider)

        # Algorithm Panel
        algorithm_panel = QGroupBox("Select Algorithm", main_widget)
        algorithm_layout = QGridLayout(algorithm_panel)

        algorithm_panel.setFixedSize(BOX_WIDTH, ALGORITHM_HEIGHT)

        bfs_button = QPushButton("BFS")
        dfs_button = QPushButton("DFS")
        ids_button = QPushButton("IDS")
        astar_man_button = QPushButton("A* (Manhattan)")
        astar_euc_button = QPushButton("A* (Euclidean)")

        self.buttons = [bfs_button, dfs_button, ids_button, astar_man_button, astar_euc_button]

        for button in self.buttons:
            button.setCheckable(True)
            button.setEnabled(False)

        bfs_button.clicked.connect(self.select_algorithm)
        dfs_button.clicked.connect(self.select_algorithm)
        ids_button.clicked.connect(self.select_algorithm)
        astar_man_button.clicked.connect(self.select_algorithm)
        astar_euc_button.clicked.connect(self.select_algorithm)

        algorithm_layout.addWidget(bfs_button, 0, 0)
        algorithm_layout.addWidget(dfs_button, 0, 1)
        algorithm_layout.addWidget(ids_button, 1, 0)
        algorithm_layout.addWidget(astar_man_button, 1, 1)
        algorithm_layout.addWidget(astar_euc_button, 2, 0)

        # Solve Panel
        solve_panel = QGroupBox(main_widget)
        solve_layout = QHBoxLayout(solve_panel)

        solve_panel.setFixedSize(BOX_WIDTH, SOLVE_HEIGHT)

        self.solve_button = QPushButton("Solve Puzzle")
        self.solve_button.setEnabled(False)

        self.solve_button.clicked.connect(self.solve_puzzle)

        solve_layout.addWidget(self.solve_button)

        content_layout.addWidget(self.puzzle_panel, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(input_panel)
        content_layout.addWidget(states_panel)
        content_layout.addWidget(algorithm_panel)
        content_layout.addWidget(solve_panel)

    def get_tiles(self):
        tiles = []

        for ch in self.input_line.text():
            if not ch.isdigit():
                return None
            tiles.append(int(ch))

        if sorted(tiles) != list(range(9)):
            return None

        return tiles

    def insert_tiles(self):
        tiles = self.get_tiles()

        if tiles is None:
            self.show_status("Invalid initial state.", "error")
            return
        else:
            self.show_status("Inserted successfully.", "success")

        self.path = None
        self.path_index = 0

        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.auto_button.setEnabled(False)

        for button in self.buttons:
            button.setEnabled(True)

        self.states_label.setText("Expanded Nodes: 0 | Path Cost: 0\n Search Depth: 0 | Number of Moves: 0 | Moves Left: 0")

        self.board = np.array(tiles).reshape(3, 3)
        self.update_tiles()

    def create_tiles(self):
        for r in range(SIZE):
            for c in range(SIZE):
                tile = QLabel()
                tile.setAlignment(Qt.AlignmentFlag.AlignCenter)
                tile.setFixedSize(TILE_SIZE, TILE_SIZE)

                self.puzzle_layout.addWidget(tile, r, c)
                self.tiles.append(tile)

    def update_tiles(self):
        tiles = self.board

        index = 0
        for r in range(SIZE):
            for c in range(SIZE):
                if tiles[r][c] != 0:
                    self.tiles[index].setText(str(tiles[r][c]))

                    self.tiles[index].setStyleSheet("""
                        background-color: #334155;
                        color: #F1F5F9;
                        font-size: 28px;
                        font-weight: bold;
                        border: 2px solid #475569;
                        border-radius: 10px;
                    """)
                else:
                    self.tiles[index].setText("")
                    self.tiles[index].setStyleSheet("""
                        background-color: transparent;
                        border: none;
                    """)

                index += 1

    def update_time(self):
        time_value = (time.perf_counter() - self.start_time) * 1000
        self.timer_label.setText(f"Search Time: {time_value:.3f} ms")

    def update_speed_label(self):
        self.speed_label.setText(f"Move Speed = {self.speed_slider.value() / MAX_DELAY_MILLISECOND:.1f} second/move")

    def select_algorithm(self):
        sender_button = self.sender()
        self.selected_algorithm = sender_button.text()

        for button in self.buttons:
            if button == sender_button:
                button.setChecked(True)

                if not self.solve_button.isEnabled():
                    self.solve_button.setEnabled(True)
            else:
                button.setChecked(False)

    def solve_puzzle(self):
        if not is_solvable(self.board):
            self.show_status("Not Solvable.", "error")
            return
        else:
            self.show_status("", "none")

        initial_state = State(self.board.copy(), 0)

        self.timer_label.setText(f"Search Time: 0 seconds")
        self.states_label.setText("Expanded Nodes: 0 | Path Cost: 0\n Search Depth: 0 | Number of Moves: 0 | Moves Left: 0")

        self.solve_button.setEnabled(False)

        self.path_index = 0
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.auto_button.setEnabled(False)
        self.insert_button.setEnabled(False)

        self.worker = RunSearch(self.algorithms[self.selected_algorithm], initial_state)

        self.start_time = time.perf_counter()
        self.timer.start(INTERVAL_MILLISECOND)
        self.worker.solved.connect(self.passed_solution)
        self.worker.failed.connect(self.fail_solution)
        self.worker.start()

    def fail_solution(self, message):
        print(message)

        self.timer.stop()
        self.solve_button.setEnabled(True)
        self.insert_button.setEnabled(True)

    def passed_solution(self, path, expansion_count, search_depth):
        self.timer.stop()

        time_value = (time.perf_counter() - self.start_time) * 1000
        self.timer_label.setText(f"Search Time: {time_value:.3f} ms")

        self.path = path
        self.expansion_count = expansion_count
        self.search_depth = search_depth

        self.show_status("Solved", "success")

        self.solve_button.setEnabled(True)
        self.insert_button.setEnabled(True)

        if len(self.path) != 1:
            self.auto_button.setEnabled(True)
            self.next_button.setEnabled(True)

        self.states_label.setText(
            f"Expanded Nodes: {self.expansion_count} | Path Cost: {self.path[-1].depth}\n" +
            f"Search Depth: {self.search_depth} | Number of Moves: {len(self.path) - 1} "+
            f"| Moves Left: {len(self.path) - 1 - self.path_index}"
        )

    def prev_move(self):
        self.path_index -= 1

        self.next_button.setEnabled(True)
        self.auto_button.setEnabled(True)

        self.show_step()

        if self.path_index == 0:
            self.prev_button.setEnabled(False)

    def next_move(self):

        self.path_index += 1

        self.prev_button.setEnabled(True)

        self.show_step()

        if self.path_index == len(self.path) - 1:
            self.next_button.setEnabled(False)
            self.auto_button.setEnabled(False)

    def auto_move(self):

        self.next_button.setEnabled(False)
        self.auto_button.setEnabled(False)
        self.prev_button.setEnabled(False)
        self.solve_button.setEnabled(False)
        self.insert_button.setEnabled(False)

        for button in self.buttons:
            button.setEnabled(False)

        self.auto_step()

    def auto_step(self):
        if self.path_index >= len(self.path) -1:
            self.prev_button.setEnabled(True)
            self.solve_button.setEnabled(True)
            self.insert_button.setEnabled(True)

            for button in self.buttons:
                button.setEnabled(True)

            return

        self.path_index += 1

        self.show_step()

        QTimer.singleShot(self.speed_slider.value(), self.auto_step)

    def closeEvent(self, event):
        if self.worker is not None and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        event.accept()

    def update_state(self):
        if not self.path:
            self.states_label.setText(
                "Expanded Nodes: 0 | Path Cost: 0\n"
                "Search Depth: 0 | Number of Moves: 0 | Moves Left: 0"
            )
            return

        self.states_label.setText(
            f"Expanded Nodes: {self.expansion_count} | Path Cost: {self.path[-1].depth}\n"
            f"Search Depth: {self.search_depth} | Number of Moves: {len(self.path) - 1} | Moves Left: {len(self.path) - 1 - self.path_index}"
        )

    def show_step(self):
        self.board = self.path[self.path_index].board
        self.update_tiles()
        self.update_state()

    def show_status(self, text, kind):
        self.system_msg.setText(text)
        self.system_msg.setStyleSheet(STATUS_STYLES[kind])