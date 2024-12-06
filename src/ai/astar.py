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
    
    def calculate_heuristic(self, pos: Tuple[int, int], goal: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> float:
        """Calculate a more sophisticated heuristic that considers snake body"""
        base_cost = self.manhattan_distance(pos, goal)
        
        # Add penalty for being near snake body (except tail which will move)
        body_penalty = 0
        for body_part in snake_body[:-1]:  # Exclude tail
            dist_to_body = self.manhattan_distance(pos, body_part)
            if dist_to_body < 2:  # Penalize being very close to snake body
                body_penalty += 2
        
        return base_cost + body_penalty

    def simulate_snake_movement(self, snake_body: List[Tuple[int, int]], new_head: Tuple[int, int], growing: bool) -> List[Tuple[int, int]]:
        """Simulate snake movement to get future snake body position"""
        new_body = [new_head] + snake_body[:-1] if not growing else [new_head] + snake_body
        return new_body

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], snake_body: List[Tuple[int, int]], is_alternative_path: bool = False) -> List[Tuple[int, int]]:
        class Node:
            def __init__(self, pos, snake_body, g_cost=0, h_cost=0, parent=None):
                self.pos = pos
                self.snake_body = snake_body
                self.g_cost = g_cost
                self.h_cost = h_cost
                self.f_cost = g_cost + h_cost
                self.parent = parent
            def __lt__(self, other):
                return self.f_cost < other.f_cost
            def __eq__(self, other):
                return self.pos == other.pos
            def __hash__(self):
                return hash(self.pos)

        start_node = Node(start, snake_body, 0, self.calculate_heuristic(start, goal, snake_body))
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
            
            # Get valid neighbors considering future snake positions
            for neighbor_pos in self.get_valid_neighbors(current.pos, current.snake_body):
                if neighbor_pos in closed_set:
                    continue
                
                # Simulate snake movement to this neighbor
                is_growing = neighbor_pos == goal
                new_snake_body = self.simulate_snake_movement(current.snake_body, neighbor_pos, is_growing)
                
                g_cost = current.g_cost + 1
                h_cost = self.calculate_heuristic(neighbor_pos, goal, new_snake_body)
                
                neighbor = Node(neighbor_pos, new_snake_body, g_cost, h_cost, current)
                
                if neighbor_pos not in came_from or g_cost < came_from[neighbor_pos].g_cost:
                    came_from[neighbor_pos] = neighbor
                    if neighbor not in open_set:
                        heapq.heappush(open_set, neighbor)
        
        # If no path found and this isn't already an alternative path search
        if not is_alternative_path:
            # Find the position closest to the goal that we can reach
            best_pos = None
            best_score = float('inf')
            for pos in self.get_valid_neighbors(start, snake_body):
                score = self.manhattan_distance(pos, goal)
                if score < best_score and pos not in closed_set:
                    best_score = score
                    best_pos = pos
            
            if best_pos:
                # Just return path to best_pos directly
                return [best_pos]
        
        return []

    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Always recalculate path to handle dynamic situations better
        self.current_path = self.find_path(snake_head, food_pos, snake_body)
        
        if self.current_path:
            next_pos = self.current_path[0]
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        
        # If no path found, try to find a safe direction that maximizes future options
        safe_moves = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (snake_head[0] + dx, snake_head[1] + dy)
            if new_pos not in snake_body and 0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size:
                # Count number of valid moves from this position
                future_options = len(self.get_valid_neighbors(new_pos, snake_body))
                safe_moves.append((future_options, (dx, dy)))
        
        if safe_moves:
            # Choose the move that gives most future options
            return max(safe_moves)[1]
        return (0, 0)  # No safe move found