from typing import List, Tuple, Set
from .base import BaseAI

class DFSAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "DFS Exploration"
        self.description = "Uses Depth-First Search for exploration"
        self.current_path = []
        self.visited: Set[Tuple[int, int]] = set()

    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        self.visited.add(snake_head)
        neighbors = self.get_valid_neighbors(snake_head, snake_body)
        
        # Clear previous path
        self.current_path = []
        
        # First try to move towards food if possible
        if food_pos in neighbors:
            self.current_path = [food_pos]
            return (food_pos[0] - snake_head[0], food_pos[1] - snake_head[1])
        
        # Prioritize unvisited neighbors
        unvisited = [n for n in neighbors if n not in self.visited]
        if unvisited:
            next_pos = unvisited[0]
            # Show the planned path
            self.current_path = [next_pos]
            # Add a few more potential future moves for visualization
            current = next_pos
            for _ in range(4):  # Look ahead 4 moves
                future_neighbors = self.get_valid_neighbors(current, snake_body)
                future_unvisited = [n for n in future_neighbors if n not in self.visited]
                if future_unvisited:
                    current = future_unvisited[0]
                    self.current_path.append(current)
                else:
                    break
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        
        # If all neighbors are visited, pick any valid one
        if neighbors:
            next_pos = neighbors[0]
            self.current_path = [next_pos]
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        
        return (0, 0)  # No valid moves

    def reset(self):
        """Reset the visited set when starting a new game"""
        self.visited.clear()
        self.current_path = []