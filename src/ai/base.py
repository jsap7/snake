from typing import List, Tuple
from src.utils.settings import GRID_SIZE

class BaseAI:
    def __init__(self, name="Base AI"):
        self.name = name
        self.description = "Base AI class"
        self.grid_size = GRID_SIZE
        self.current_path = []  # For visualization
        
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        raise NotImplementedError

    def get_valid_neighbors(self, pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Get valid neighboring positions"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if (0 <= new_pos[0] < self.grid_size and 
                0 <= new_pos[1] < self.grid_size and 
                new_pos not in snake_body):
                neighbors.append(new_pos)
        return neighbors 