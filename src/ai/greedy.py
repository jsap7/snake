from typing import List, Tuple
import heapq
from .base import BaseAI

class GreedyBestFirstAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "Greedy Best-First"
        self.description = "Always moves towards food using Manhattan distance"
        self.current_path = []
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        # Priority queue of (distance, position, path)
        queue = [(self.manhattan_distance(start, goal), start, [])]
        visited = {start}
        
        while queue:
            _, current, path = heapq.heappop(queue)
            
            if current == goal:
                return path + [current]
            
            # Get valid neighbors
            neighbors = self.get_valid_neighbors(current, snake_body)
            
            # Add neighbors to queue with their distance to goal
            for next_pos in neighbors:
                if next_pos not in visited:
                    visited.add(next_pos)
                    new_path = path + [current]
                    # Priority is just the Manhattan distance to goal (greedy approach)
                    priority = self.manhattan_distance(next_pos, goal)
                    heapq.heappush(queue, (priority, next_pos, new_path))
        
        return []
    
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Find path to food
        path = self.find_path(snake_head, food_pos, snake_body)
        
        # Update current_path for visualization
        self.current_path = path[1:] if len(path) > 1 else []
        
        # If path found, move towards first position
        if path and len(path) > 1:
            next_pos = path[1]  # First position after current position
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        
        # If no path found, try to find any safe move
        neighbors = self.get_valid_neighbors(snake_head, snake_body)
        if neighbors:
            next_pos = min(neighbors, key=lambda pos: self.manhattan_distance(pos, food_pos))
            self.current_path = [next_pos]
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        
        return (0, 0)  # No valid moves 