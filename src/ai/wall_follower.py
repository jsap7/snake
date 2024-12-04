from typing import List, Tuple, Set
from .base import BaseAI
from src.utils.settings import GRID_SIZE

class WallFollowerAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "Wall Follower"
        self.description = "Follows walls and edges of the grid"
        self.current_path = []
        self.current_direction = (1, 0)  # Start moving right
        self.preferred_side = "right"  # Follow right wall by default
    
    def is_wall(self, pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> bool:
        """Check if a position is a wall (grid boundary or snake body)"""
        x, y = pos
        return (x < 0 or x >= GRID_SIZE or 
                y < 0 or y >= GRID_SIZE or 
                pos in snake_body)
    
    def find_nearest_wall(self, pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Find direction to nearest wall or edge"""
        # Check all directions and find closest wall
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        min_dist = float('inf')
        best_direction = directions[0]
        
        for dx, dy in directions:
            dist = 0
            current = pos
            while not self.is_wall((current[0] + dx, current[1] + dy), snake_body):
                dist += 1
                current = (current[0] + dx, current[1] + dy)
            
            if dist < min_dist:
                min_dist = dist
                best_direction = (dx, dy)
        
        return best_direction
    
    def has_wall_on_side(self, pos: Tuple[int, int], direction: Tuple[int, int], snake_body: List[Tuple[int, int]], side: str) -> bool:
        """Check if there's a wall on the specified side relative to current direction"""
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        current_idx = directions.index(direction)
        
        # Get the direction to check (right or left of current direction)
        check_idx = (current_idx + (1 if side == "right" else -1)) % 4
        check_direction = directions[check_idx]
        
        # Position to check for wall
        check_pos = (pos[0] + check_direction[0], pos[1] + check_direction[1])
        return self.is_wall(check_pos, snake_body)
    
    def get_next_direction(self, current_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Get next direction following wall on preferred side"""
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        current_idx = directions.index(self.current_direction)
        
        # Check if we're following a wall
        has_wall = self.has_wall_on_side(current_pos, self.current_direction, snake_body, self.preferred_side)
        
        if not has_wall:
            # If we're not following a wall, find the nearest one
            wall_direction = self.find_nearest_wall(current_pos, snake_body)
            # If the nearest wall isn't in our current direction, turn towards it
            if wall_direction != self.current_direction:
                return wall_direction
        
        # If we're following a wall or heading towards one
        if has_wall:
            # Try to continue forward while keeping wall on preferred side
            forward_pos = (current_pos[0] + self.current_direction[0],
                         current_pos[1] + self.current_direction[1])
            if not self.is_wall(forward_pos, snake_body):
                return self.current_direction
        
        # If we can't go forward, try turning while maintaining wall contact
        if self.preferred_side == "right":
            turn_sequence = [(current_idx + i) % 4 for i in [-1, 1, 2]]  # left, right, back
        else:
            turn_sequence = [(current_idx + i) % 4 for i in [1, -1, 2]]  # right, left, back
        
        for turn in turn_sequence:
            new_direction = directions[turn]
            new_pos = (current_pos[0] + new_direction[0],
                      current_pos[1] + new_direction[1])
            if not self.is_wall(new_pos, snake_body):
                return new_direction
        
        return self.current_direction
    
    def look_ahead(self, pos: Tuple[int, int], direction: Tuple[int, int], snake_body: List[Tuple[int, int]], steps: int = 10) -> List[Tuple[int, int]]:
        """Look ahead several steps to show planned path"""
        path = []
        current_pos = pos
        current_direction = direction
        temp_body = snake_body.copy()
        
        for _ in range(steps):
            next_pos = (current_pos[0] + current_direction[0],
                       current_pos[1] + current_direction[1])
            
            if self.is_wall(next_pos, temp_body):
                break
            
            path.append(next_pos)
            current_pos = next_pos
            temp_body = temp_body[:-1] + [next_pos]
            current_direction = self.get_next_direction(current_pos, temp_body)
        
        return path
    
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # If food is adjacent and reachable, go for it
        neighbors = self.get_valid_neighbors(snake_head, snake_body)
        if food_pos in neighbors:
            self.current_path = [food_pos]
            return (food_pos[0] - snake_head[0], food_pos[1] - snake_head[1])
        
        # Get next direction following the wall
        self.current_direction = self.get_next_direction(snake_head, snake_body)
        
        # Look ahead and update current_path for visualization
        self.current_path = self.look_ahead(snake_head, self.current_direction, snake_body)
        
        return self.current_direction