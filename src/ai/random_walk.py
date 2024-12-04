from typing import List, Tuple
import random
from src.ai.base import BaseAI

class RandomWalkAI(BaseAI):
    def __init__(self):
        super().__init__("random")
        self.name = "Random Walk"
        self.description = "Makes random valid moves"
        self.current_path = []

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
            
            # Add the chosen position to current_path
            self.current_path = [next_pos]
            
            # Add a few potential future moves for visualization
            current = next_pos
            temp_body = snake_body[:-1] + [next_pos]  # Simulate snake's next position
            
            for _ in range(4):  # Look ahead 4 moves
                future_neighbors = self.get_valid_neighbors(current, temp_body)
                if future_neighbors:
                    future_pos = random.choice(future_neighbors)
                    self.current_path.append(future_pos)
                    current = future_pos
                    temp_body = temp_body[:-1] + [future_pos]
                else:
                    break
            
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        return (0, 0)  # No valid moves available