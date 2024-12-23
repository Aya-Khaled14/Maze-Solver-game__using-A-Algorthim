# Maze-Solver-game__using-A-Algorthim
# Maze Solver with A* Algorithm

## Project Description

This Python-based **Maze Solver** application utilizes the A* algorithm to find the shortest path between a start and end point in a customizable grid maze. The application features an interactive grid where users can place walls, select start and end points, and visualize the A* algorithm in action.

---

## Features

### Grid and Visualization
- **Dynamic Grid**: A 25x25 grid where each cell can be edited to create walls or pathways.
- **Real-Time Updates**: Visual representation of the A* algorithm’s progress, including explored nodes and the shortest path.
- **Color Coding**:
  - **White**: Unexplored cells.
  - **Black**: Walls/obstacles.
  - **Green**: Start point.
  - **Red**: End point.
  - **Blue**: Shortest path.
  - **Yellow**: Nodes being explored.
  - **Dark Blue**: Current node under processing.

### User Interaction
- **Wall Placement**: Left-click to place walls, right-click to remove them.
- **Start and End Selection**: Keyboard shortcuts to set the start (`B`) and end (`E`) points dynamically.
- **Instructions**: Clear, easy-to-read instructions displayed at the bottom of the screen.

### A* Algorithm
- **Heuristic-Based**: Implements Manhattan distance for efficient pathfinding.
- **Obstacle Handling**: Dynamically avoids walls and recalculates paths.
- **No Path Detection**: Notifies users if no valid path exists between the start and end points.

### Controls
- **Mouse Actions**:
  - Left-click: Place walls.
  - Right-click: Remove walls.
- **Keyboard Shortcuts**:
  - `SPACE`: Start the A* algorithm.
  - `B`: Enter start point selection mode.
  - `E`: Enter end point selection mode.
  - `R`: Reset the grid and selections.

---

## Technologies Used
- **Python**: For logic and application flow.
- **Pygame**: For graphical interface and real-time visualization.
- **Heapq**: For efficient priority queue management in the A* algorithm.

---

## How to Run
1. Install Python and Pygame:
   ```bash
   pip install pygame
