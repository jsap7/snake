import random
from typing import List, Tuple, Optional
from src.utils.settings import GRID_SIZE

class Food:
    def __init__(self):
        self.position = self.spawn()
    
    def spawn(self, snake_body: Optional[List[Tuple[int, int]]] = None) -> Tuple[int, int]:
        """Spawn food in a random position, avoiding the snake's body"""
        if snake_body is None:
            snake_body = []
        
        # Get all possible positions
        all_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
        
        # Remove snake body positions
        available_positions = [pos for pos in all_positions if pos not in snake_body]
        
        if available_positions:
            self.position = random.choice(available_positions)
        else:
            # If no positions available (snake fills grid), put food at impossible position
            self.position = (-1, -1)
        
        return self.position
