from src.ai.base import BaseAI
from src.ai.astar import AStarAI
from src.ai.hamiltonian import HamiltonianWithShortcutsAI
from typing import Tuple, List, Optional, Set, Dict
from src.utils.settings import GRID_SIZE
from collections import deque

class SmartHybridAI(BaseAI):
    def __init__(self):
        super().__init__("smart_hybrid")
        self.name = "Smart Hybrid"
        self.description = "Advanced hybrid of A* and Hamiltonian with optimized performance"
        self.astar = AStarAI()
        self.hamiltonian = HamiltonianWithShortcutsAI()
        self.current_strategy = "astar"
        self.grid_size = GRID_SIZE
        self.safety_margin = 2
        self.space_score_cache: Dict[Tuple[Tuple[int, int], Tuple[Tuple[int, int], ...]], float] = {}
        
    def calculate_space_score(self, pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> float:
        """Calculate available space score with flood fill and caching"""
        # Convert snake_body to tuple for hashing
        cache_key = (pos, tuple(snake_body))
        if cache_key in self.space_score_cache:
            return self.space_score_cache[cache_key]
            
        visited = {pos}
        queue = deque([pos])
        space_score = 0
        depth = 0
        max_depth = 4  # Reduced depth for performance
        
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
                        space_score += 1.0 / depth
        
        self.space_score_cache[cache_key] = space_score
        if len(self.space_score_cache) > 1000:  # Prevent memory bloat
            self.space_score_cache.clear()
        return space_score
    
    def validate_path(self, path: List[Tuple[int, int]], snake_body: List[Tuple[int, int]]) -> bool:
        """Validate path safety with optimized checks"""
        if not path:
            return False
            
        temp_body = snake_body.copy()
        
        # Only check first few positions for performance
        check_positions = path[:4]  # Reduced from checking entire path
        
        for pos in check_positions:
            # Update snake body
            temp_body = temp_body[1:] + [pos]
            
            # Quick neighbor check first (faster than space score)
            neighbors = self.get_valid_neighbors(pos, temp_body)
            if len(neighbors) < 2:  # Need at least 2 escape routes
                return False
            
            # Only calculate space score if we pass neighbor check
            space_score = self.calculate_space_score(pos, temp_body)
            if space_score < 4:  # Slightly reduced threshold for performance
                return False
        
        return True
    
    def should_use_astar(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], 
                        snake_body: List[Tuple[int, int]], astar_path: List[Tuple[int, int]]) -> bool:
        """Optimized strategy decision making"""
        snake_length = len(snake_body)
        grid_area = self.grid_size ** 2
        
        # Quick early checks
        if not astar_path:
            return False
            
        # Early game: Be aggressive
        if snake_length < grid_area * 0.3:
            return self.validate_path(astar_path, snake_body)
        
        # Late game: Use Hamiltonian
        if snake_length > grid_area * 0.6:
            return False
        
        # Mid game: More careful validation
        if not self.validate_path(astar_path, snake_body):
            return False
            
        # Final space check
        space_score = self.calculate_space_score(snake_head, snake_body)
        return space_score > 6 and len(astar_path) < grid_area * 0.2
    
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