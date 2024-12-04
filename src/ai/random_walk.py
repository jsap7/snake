from typing import List, Tuple
import random
from .base import BaseAI

class RandomAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "Random Walk"
        self.description = "Makes random valid moves"
        self.current_path = []  # For visualization

    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        valid_neighbors = self.get_valid_neighbors(snake_head, snake_body)
        
        # Clear previous path
        self.current_path = []
        
        if valid_neighbors:
            # Try to move towards food if it's a valid neighbor
            if food_pos in valid_neighbors:
                next_pos = food_pos
            else:
                next_pos = random.choice(valid_neighbors)
            
            # Add the chosen position to current_path for visualization
            self.current_path = [next_pos]
            
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        return (0, 0)  # No valid moves available 