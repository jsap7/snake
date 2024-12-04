# AI Snake Game

A Python implementation of the classic Snake game with multiple AI algorithms and visualization. This project demonstrates different pathfinding and decision-making algorithms in a visual and interactive way.

## Features

- Classic snake game with modern graphics
- Multiple AI algorithms:
  - A* Pathfinding
  - BFS (Breadth-First Search)
  - Hamiltonian Cycle with Shortcuts
  - DFS (Depth-First Search)
  - Random Walk
- Real-time path visualization
- Performance statistics tracking
- Beautiful UI with smooth animations
- Both human and AI control modes

## Project Structure

```
snake/
├── src/
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── astar.py
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── hamiltonian.py
│   │   └── random_walk.py
│   ├── game/
│   │   ├── __init__.py
│   │   ├── food.py
│   │   ├── snake.py
│   │   └── game_state.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── renderer.py
│   │   ├── launcher.py
│   │   ├── game_stats.py
│   │   └── themes/
│   │       └── azure.tcl
│   └── utils/
│       ├── __init__.py
│       ├── settings.py
│       └── input_handler.py
├── requirements.txt
├── main.py
├── LICENSE
└── README.md
```

## Requirements

- Python 3.8+
- Pygame
- Tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jsap7/snake-ai.git
cd snake-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the game:
```bash
python main.py
```

### Controls

- Arrow keys or WASD: Control snake (in human mode)
- Space: Start game / Restart after game over
- Tab: Toggle between human and AI control
- 1-5: Select different AI algorithms
- Esc: Quit game

## AI Algorithms

1. **A* Pathfinding**
   - Finds optimal path to food using Manhattan distance heuristic
   - Visualizes planned path in real-time
   - Highly efficient for shorter snake lengths

2. **BFS (Breadth-First Search)**
   - Guarantees shortest path to food
   - Explores grid systematically
   - Good for avoiding traps

3. **Hamiltonian Cycle with Shortcuts**
   - Follows a safe Hamiltonian cycle
   - Takes shortcuts when possible
   - Never dies but may not be the most efficient

4. **DFS (Depth-First Search)**
   - Explores paths deeply before backtracking
   - Interesting to watch but not optimal
   - Good for demonstration purposes

5. **Random Walk**
   - Makes random valid moves
   - Used as a baseline for comparison
   - Demonstrates importance of strategy

## Statistics Tracked

- Score
- Turns made (direction changes)
- Cells traveled
- Efficiency ratio
- Time elapsed
- High score