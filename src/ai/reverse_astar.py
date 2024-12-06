from typing import List, Tuple, Dict, Set
import heapq
from .base import BaseAI

class ReverseAStarAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "Reverse A* (Longest Path)"
        self.description = "Finds longest valid path using reversed A* algorithm"
        self.reset_path()
    
    def reset_path(self):
        """Reset the current path when a new game starts or when path is invalid"""
        self.current_path = []
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        class Node:
            def __init__(self, pos, path_length=0, parent=None):
                self.pos = pos
                self.path_length = path_length
                self.parent = parent
            def __lt__(self, other):
                return self.path_length > other.path_length  # Maximize path length

        # Priority queue using negative path length to find longest path
        open_set = [(0, 0, Node(start))]  # (priority, tiebreaker, node)
        closed_set: Set[Tuple[int, int]] = set()
        came_from: Dict[Tuple[int, int], Node] = {start: Node(start)}
        
        while open_set:
            _, _, current = heapq.heappop(open_set)
            
            if current.pos == goal:
                path = []
                while current.pos != start:
                    path.append(current.pos)
                    current = current.parent
                path.reverse()
                return path
                
            if current.pos in closed_set:
                continue
                
            closed_set.add(current.pos)
            
            # Get valid neighbors
            neighbors = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_pos = (current.pos[0] + dx, current.pos[1] + dy)
                if (0 <= new_pos[0] < self.grid_size and 
                    0 <= new_pos[1] < self.grid_size and 
                    new_pos not in snake_body and
                    new_pos not in closed_set):
                    neighbors.append(new_pos)
            
            # Sort neighbors by distance from goal (prefer further positions)
            neighbors.sort(key=lambda x: -self.manhattan_distance(x, goal))
            
            for neighbor_pos in neighbors:
                path_length = current.path_length + 1
                
                if (neighbor_pos not in came_from or 
                    path_length > came_from[neighbor_pos].path_length):
                    neighbor = Node(neighbor_pos, path_length, current)
                    came_from[neighbor_pos] = neighbor
                    
                    # Priority is negative path length to make it a longest path search
                    # Add manhattan distance as tiebreaker to prefer paths away from goal
                    priority = -path_length
                    tiebreaker = -self.manhattan_distance(neighbor_pos, goal)
                    heapq.heappush(open_set, (priority, tiebreaker, neighbor))
        
        # If no path found, reset the current path
        self.reset_path()
        return []

    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Reset path if the current path is invalid
        if self.current_path:
            next_pos = self.current_path[0]
            if (next_pos in snake_body or 
                not (0 <= next_pos[0] < self.grid_size and 0 <= next_pos[1] < self.grid_size)):
                self.reset_path()
        
        if not self.current_path:
            self.current_path = self.find_path(snake_head, food_pos, snake_body)
        
        if self.current_path:
            next_pos = self.current_path.pop(0)
            dx = next_pos[0] - snake_head[0]
            dy = next_pos[1] - snake_head[1]
            return (dx, dy)
        
        # If no path found, try to find a direction that maximizes distance from food
        best_direction = (0, 0)
        max_distance = -1
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (snake_head[0] + dx, snake_head[1] + dy)
            if (0 <= new_pos[0] < self.grid_size and 
                0 <= new_pos[1] < self.grid_size and 
                new_pos not in snake_body):
                distance = self.manhattan_distance(new_pos, food_pos)
                if distance > max_distance:
                    max_distance = distance
                    best_direction = (dx, dy)
        
        return best_direction