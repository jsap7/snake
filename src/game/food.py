import random
from typing import List, Tuple, Optional
from src.utils.settings import GRID_SIZE

class Food:
    def __init__(self):
        # Start food away from snake's initial position
        self.position = (GRID_SIZE - 5, GRID_SIZE - 5)
    
    def spawn(self, snake_body: Optional[List[Tuple[int, int]]] = None) -> Tuple[int, int]:
        """Spawn food in a random position, avoiding the snake's body"""
        if snake_body is None:
            snake_body = []
        
        # Get all possible positions
        all_positions = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
        
        # Remove snake body positions
        available_positions = [pos for pos in all_positions if pos not in snake_body]
        
        if available_positions:
            # Try to spawn food at least 3 cells away from snake head if possible
            if snake_body:
                snake_head = snake_body[0]
                distant_positions = [
                    pos for pos in available_positions 
                    if abs(pos[0] - snake_head[0]) + abs(pos[1] - snake_head[1]) > 3
                ]
                if distant_positions:
                    self.position = random.choice(distant_positions)
                else:
                    self.position = random.choice(available_positions)
            else:
                self.position = random.choice(available_positions)
        else:
            # If no positions available (snake fills grid), put food at impossible position
            self.position = (-1, -1)
        
        return self.position
