# 8-Puzzle-Solver

A Python-based 8-Puzzle Solver that allow users to solve the puzzle with any initial state with different algorithms, that search for the goal state, through an interactive graphical interface.

## Overview

The 8-Puzzle is a game consisting of 3x3 board with eight numbered tiles and one blank space, the only way to solve this puzzle is to rearrange the tiles into their goal by moving tiles into the blank space.

This project is a solver for that game, that search for the right path to solve the puzzle, the search method can be done
using different algorithms such as Breadth First Search (BFS), Depth First Search (DFS), Iterative Deepening Search (IDS), 
and two A* algorithms each use different heuristic functions.

## Features

- Interactive Graphical Interface
- Puzzle Board updates while solving
- Input System handle the invalid board, and unsolvable ones
- States Panel allows users to see the states of the solution, and control the board
  - Search Time
  - Number of Expanded Nodes
  - Cost of The Solution Path
  - Max Depths achieved while searching
  - Total Number of Moves to solve this puzzle
  - Number of Moves Left while solving the puzzle
  - Next Button to move to the next step
  - Previous Button to move to the previous step
  - Auto Solve Button will move the board automatically until the goal state with a delay
  - Slider controls the delay of the auto solve movement
- Algorithms Panel allows user to select the searching algorithms
  - BFS
  - DFS
  - IDS
  - A* (Manhattan)
  - A* (Euclidean)
- Solve Button to start the solving process

## Technologies Used

- Python (Programming Language)
- NumPy (Library)
- PySide6 (GUI Library)

# 8-Puzzle Solver

A Python-based 8-Puzzle Solver that allows users to solve the classic sliding puzzle using different search algorithms through an interactive graphical interface.

## Overview

The 8-Puzzle is a sliding puzzle consisting of a 3×3 board with eight numbered tiles and one empty space. The objective is to rearrange the tiles into their goal configuration by moving tiles into the empty space.

This project implements several AI search algorithms to solve the puzzle and provides a graphical interface to visualize the solution step by step.

## Goal State

```text
0 1 2
3 4 5
6 7 8
```
The blank is represented by 0

## Features

- Interactive graphical user interface built with **PySide6**
- Multiple search algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Iterative Deepening Search (IDS)
  - A* Search with Manhattan Distance heuristic
- Step-by-step solution visualization
- Automatic solution playback
- Search execution time measurement
- Move counter and solution navigation
- Initial state input and validation
- Puzzle solvability detection

## Technologies Used

- Python
- NumPy
- PySide6

## Installation

1. Clone the repository:
    ```bash
      git clone https://github.com/Mina-Ihab/8-Puzzle-Solver.git
   ```
2. Navigate to the project directory:
    ```bash
      cd 8-Puzzle-Solver  
   ```
3. Create an environment:
    ```bash
      python -m venve environment_name
   ```
4. Activate the environment:
    ```bash
      environment_name\Scripts\activate
   ```
5. Install the required dependencies:
    ```bash
      pip install -r requirement.txt
   ```
   
## Usage

1. Run the application
    ```bash
     python main.py
   ```
2. Insert a puzzle initial state.
3. Select an algorithm.
4. Start the solving process.
5. Navigate through the solution or use auto solve to visualize the moves.

