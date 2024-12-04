from typing import List, Tuple, Dict, Set
import heapq
from .base import BaseAI

class AStarAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "A* Pathfinding"
        self.description = "Finds optimal path using A* algorithm"
        self.current_path = []
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        class Node:
            def __init__(self, pos, g_cost=0, h_cost=0, parent=None):
                self.pos = pos
                self.g_cost = g_cost
                self.h_cost = h_cost
                self.f_cost = g_cost + h_cost
                self.parent = parent
            def __lt__(self, other):
                return self.f_cost < other.f_cost

        start_node = Node(start, 0, self.manhattan_distance(start, goal))
        open_set = [start_node]
        closed_set: Set[Tuple[int, int]] = set()
        came_from: Dict[Tuple[int, int], Node] = {start: start_node}
        
        while open_set:
            current = heapq.heappop(open_set)
            if current.pos == goal:
                path = []
                while current.pos != start:
                    path.append(current.pos)
                    current = current.parent
                path.reverse()
                return path
                
            closed_set.add(current.pos)
            
            for neighbor_pos in self.get_valid_neighbors(current.pos, snake_body):
                if neighbor_pos in closed_set:
                    continue
                    
                g_cost = current.g_cost + 1
                h_cost = self.manhattan_distance(neighbor_pos, goal)
                
                neighbor = Node(neighbor_pos, g_cost, h_cost, current)
                
                if neighbor_pos not in came_from or g_cost < came_from[neighbor_pos].g_cost:
                    came_from[neighbor_pos] = neighbor
                    if neighbor not in open_set:
                        heapq.heappush(open_set, neighbor)
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
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (snake_head[0] + dx, snake_head[1] + dy)
            if new_pos not in snake_body and 0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size:
                return (dx, dy)
        return (0, 0)  # No safe move found 