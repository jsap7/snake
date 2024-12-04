from typing import List, Tuple
from collections import deque
from .base import BaseAI

class BFSAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "BFS Pathfinding"
        self.description = "Uses Breadth-First Search to find path to food"
        self.current_path = []

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        queue = deque([(start, [])])
        visited = {start}
        
        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path
                
            for next_pos in self.get_valid_neighbors(current, snake_body):
                if next_pos not in visited:
                    visited.add(next_pos)
                    new_path = path + [next_pos]
                    queue.append((next_pos, new_path))
        return []

    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        if not self.current_path:
            self.current_path = self.find_path(snake_head, food_pos, snake_body)
        
        if self.current_path:
            next_pos = self.current_path.pop(0)
            dx = next_pos[0] - snake_head[0]
            dy = next_pos[1] - snake_head[1]
            return (dx, dy)
        
        # If no path found, try to find a safe direction
        neighbors = self.get_valid_neighbors(snake_head, snake_body)
        if neighbors:
            next_pos = neighbors[0]
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        return (0, 0) 