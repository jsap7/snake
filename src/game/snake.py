from typing import List, Tuple
from src.utils.settings import GRID_SIZE

class Snake:
    def __init__(self):
        self.body = [(GRID_SIZE // 2, GRID_SIZE // 2)]  # Start in middle of grid
        self.direction = "RIGHT"
        self.turns = 0  # Track direction changes
        self.growing = False
        self.has_eaten = False  # Flag for tracking food consumption
    
    def set_direction(self, new_direction):
        if new_direction != self.direction:
            # Only count as turn if direction actually changes
            valid_change = (
                (new_direction == "UP" and self.direction != "DOWN") or
                (new_direction == "DOWN" and self.direction != "UP") or
                (new_direction == "LEFT" and self.direction != "RIGHT") or
                (new_direction == "RIGHT" and self.direction != "LEFT")
            )
            if valid_change:
                self.direction = new_direction
                self.turns += 1
                return True
        return False
    
    def move(self) -> bool:
        """Move the snake in the current direction. Returns False if collision occurs."""
        head = self.body[0]
        
        # Calculate new head position based on direction
        if self.direction == "UP":
            new_head = (head[0], head[1] - 1)
        elif self.direction == "DOWN":
            new_head = (head[0], head[1] + 1)
        elif self.direction == "LEFT":
            new_head = (head[0] - 1, head[1])
        else:  # RIGHT
            new_head = (head[0] + 1, head[1])
        
        # Check for collisions with walls
        if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
            return False
        
        # Check for collisions with self (excluding tail if not growing)
        if new_head in self.body[:-1] or (new_head in self.body and not self.growing):
            return False
        
        # Add new head
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False
            self.has_eaten = True  # Set eaten flag when growing
        
        return True
    
    def grow(self):
        """Mark the snake to grow on next move"""
        self.growing = True
    
    def get_turns(self) -> int:
        """Get the number of turns (direction changes) made"""
        return self.turns
