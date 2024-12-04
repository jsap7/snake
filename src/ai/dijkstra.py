from typing import List, Tuple, Dict, Set
import heapq
from .base import BaseAI

class DijkstraAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "Dijkstra"
        self.description = "Finds shortest path without heuristics"
        self.current_path = []
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        # Priority queue of (cost, position, path)
        queue = [(0, start, [])]
        visited: Set[Tuple[int, int]] = {start}
        costs: Dict[Tuple[int, int], int] = {start: 0}
        
        while queue:
            current_cost, current, path = heapq.heappop(queue)
            
            if current == goal:
                return path + [current]
            
            # Get valid neighbors
            neighbors = self.get_valid_neighbors(current, snake_body)
            
            # Add neighbors to queue with cumulative cost
            for next_pos in neighbors:
                new_cost = current_cost + 1  # Each step costs 1
                
                if next_pos not in costs or new_cost < costs[next_pos]:
                    costs[next_pos] = new_cost
                    visited.add(next_pos)
                    new_path = path + [current]
                    heapq.heappush(queue, (new_cost, next_pos, new_path))
        
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
            # Without heuristics, just pick the first safe neighbor
            next_pos = neighbors[0]
            self.current_path = [next_pos]
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        
        return (0, 0)  # No valid moves 