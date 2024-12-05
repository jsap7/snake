from src.ai.base import BaseAI
from src.ai.astar import AStarAI
from src.ai.hamiltonian import HamiltonianWithShortcutsAI
from typing import Tuple, List, Optional, Set
from src.utils.settings import GRID_SIZE
from collections import deque

class SmartHybridAI(BaseAI):
    def __init__(self):
        super().__init__("smart_hybrid")
        self.name = "Smart Hybrid"
        self.description = "Advanced hybrid of A* and Hamiltonian with guaranteed escape paths"
        self.astar = AStarAI()
        self.hamiltonian = HamiltonianWithShortcutsAI()
        self.current_strategy = "astar"
        self.grid_size = GRID_SIZE
        self.last_food_distance = 0
        self.consecutive_food_distance_increases = 0
        self.safety_margin = 2
        
    def find_escape_path(self, start: Tuple[int, int], snake_body: List[Tuple[int, int]], 
                        min_path_length: int = 5) -> List[Tuple[int, int]]:
        """Find a path to a safe area with minimum length"""
        queue = deque([(start, [start])])
        visited = {start}
        best_path = []
        max_space_score = 0
        
        while queue:
            current, path = queue.popleft()
            
            # Calculate space score for current position
            space_score = self.calculate_space_score(current, snake_body)
            
            # If we found a path of sufficient length to an open area
            if len(path) >= min_path_length and space_score > max_space_score:
                best_path = path
                max_space_score = space_score
            
            # Add neighbors to queue
            for next_pos in self.get_valid_neighbors(current, snake_body):
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        
        return best_path

    def has_escape_path(self, pos: Tuple[int, int], snake_body: List[Tuple[int, int]], 
                       min_length: int = 5) -> bool:
        """Check if position has an escape path of minimum length"""
        escape_path = self.find_escape_path(pos, snake_body, min_length)
        return len(escape_path) >= min_length
    
    def calculate_space_score(self, pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> float:
        """Calculate available space score with flood fill"""
        visited = {pos}
        queue = deque([pos])
        space_score = 0
        depth = 0
        max_depth = 5  # Limit depth of flood fill
        
        while queue and depth < max_depth:
            level_size = len(queue)
            depth += 1
            
            for _ in range(level_size):
                current = queue.popleft()
                neighbors = self.get_valid_neighbors(current, snake_body)
                
                for neighbor in neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        # Weight closer spaces more heavily
                        space_score += 1.0 / depth
        
        return space_score
    
    def validate_path(self, path: List[Tuple[int, int]], snake_body: List[Tuple[int, int]]) -> bool:
        """Validate that a path maintains escape routes"""
        if not path:
            return False
            
        temp_body = snake_body.copy()
        
        # Check each step along the path
        for i, pos in enumerate(path):
            # Update snake body for this step
            temp_body = temp_body[1:] + [pos]
            
            # For immediate next position, require more stringent safety
            if i == 0:
                if not self.has_escape_path(pos, temp_body, min_length=6):
                    return False
            # For future positions, ensure basic escape exists
            elif not self.has_escape_path(pos, temp_body, min_length=4):
                return False
            
            # Ensure sufficient space around position
            space_score = self.calculate_space_score(pos, temp_body)
            if space_score < 5:
                return False
        
        return True
    
    def should_use_astar(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], 
                        snake_body: List[Tuple[int, int]], astar_path: List[Tuple[int, int]]) -> bool:
        """Determine if A* is safe to use"""
        snake_length = len(snake_body)
        grid_area = self.grid_size ** 2
        
        # Early game: Be aggressive but safe
        if snake_length < grid_area * 0.3:
            return self.validate_path(astar_path, snake_body)
        
        # Late game: Use Hamiltonian
        if snake_length > grid_area * 0.6:
            return False
        
        # Mid game: Be very careful
        if not astar_path or not self.validate_path(astar_path, snake_body):
            return False
        
        # Additional mid-game safety checks
        space_score = self.calculate_space_score(snake_head, snake_body)
        return (space_score > 8 and 
                len(astar_path) < grid_area * 0.2 and
                self.has_escape_path(astar_path[-1], snake_body + astar_path[:-1], min_length=6))
    
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], 
                      snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Try A* path first
        self.astar.current_path = []
        astar_move = self.astar.get_next_move(snake_head, food_pos, snake_body)
        astar_path = self.astar.current_path
        
        # Decide which strategy to use
        if self.should_use_astar(snake_head, food_pos, snake_body, astar_path):
            self.current_strategy = "astar"
            self.current_path = astar_path
            return astar_move
        else:
            self.current_strategy = "hamiltonian"
            move = self.hamiltonian.get_next_move(snake_head, food_pos, snake_body)
            self.current_path = self.hamiltonian.current_path
            return move

# Create an alias for backward compatibility
HybridAI = SmartHybridAI