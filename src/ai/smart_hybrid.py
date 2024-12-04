from typing import List, Tuple, Set
from .base import BaseAI
from .astar import AStarAI
from .wall_follower import WallFollowerAI
from .hamiltonian import HamiltonianWithShortcutsAI
from src.utils.settings import GRID_SIZE

class SmartHybridAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "Smart Hybrid"
        self.description = "Advanced multi-strategy snake AI"
        self.current_path = []
        self.astar = AStarAI()
        self.wall_follower = WallFollowerAI()
        self.hamiltonian = HamiltonianWithShortcutsAI()
        self.current_strategy = "astar"
        self.last_food_distance = 0
        self.stuck_count = 0
    
    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def is_move_safe(self, next_pos: Tuple[int, int], snake_body: List[Tuple[int, int]], look_ahead: int = 2) -> bool:
        """Check if a move is safe by looking ahead several steps"""
        # First check immediate collision
        if next_pos in snake_body[:-1]:  # Exclude tail as it will move
            return False
            
        x, y = next_pos
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return False
            
        # Look ahead to check if we might get trapped
        available_spaces = self.flood_fill(next_pos, snake_body[:-1])
        min_safe_spaces = len(snake_body) + look_ahead
        
        return available_spaces >= min_safe_spaces
    
    def flood_fill(self, start: Tuple[int, int], obstacles: List[Tuple[int, int]]) -> int:
        """Count available spaces using flood fill algorithm"""
        if start in obstacles:
            return 0
            
        visited = {start}
        queue = [start]
        count = 1
        
        while queue:
            current = queue.pop(0)
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                x, y = next_pos
                
                if (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and 
                    next_pos not in visited and 
                    next_pos not in obstacles):
                    visited.add(next_pos)
                    queue.append(next_pos)
                    count += 1
        
        return count
    
    def is_path_safe(self, path: List[Tuple[int, int]], snake_body: List[Tuple[int, int]]) -> bool:
        """Check if entire path is safe"""
        if not path:
            return False
            
        temp_body = snake_body.copy()
        for pos in path:
            if not self.is_move_safe(pos, temp_body):
                return False
            temp_body = temp_body[1:] + [pos]
        
        return True
    
    def detect_stuck(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int]) -> bool:
        """Detect if snake is stuck in a pattern"""
        current_distance = self.manhattan_distance(snake_head, food_pos)
        is_stuck = current_distance >= self.last_food_distance
        self.last_food_distance = current_distance
        
        if is_stuck:
            self.stuck_count += 1
        else:
            self.stuck_count = 0
            
        return self.stuck_count > 5
    
    def choose_strategy(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], 
                       snake_body: List[Tuple[int, int]]) -> str:
        """Choose the best strategy based on current situation"""
        snake_length = len(snake_body)
        grid_area = GRID_SIZE * GRID_SIZE
        
        # Try A* first
        astar_path = self.astar.find_path(snake_head, food_pos, snake_body)
        if astar_path and self.is_path_safe(astar_path, snake_body):
            self.stuck_count = 0  # Reset stuck counter if we have a good path
            return "astar"
        
        # If snake is very long, use Hamiltonian
        if snake_length > grid_area * 0.85:  # Increased threshold
            return "hamiltonian"
        
        # Check if we're stuck in a pattern
        if self.detect_stuck(snake_head, food_pos):
            # Try wall following to break out of pattern
            return "wall_follower"
        
        # Default to A* even if path isn't perfect
        return "astar"
    
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], 
                      snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Choose the best strategy for current situation
        self.current_strategy = self.choose_strategy(snake_head, food_pos, snake_body)
        
        # Get path based on chosen strategy
        if self.current_strategy == "astar":
            move = self.astar.get_next_move(snake_head, food_pos, snake_body)
            self.current_path = self.astar.current_path
        elif self.current_strategy == "wall_follower":
            move = self.wall_follower.get_next_move(snake_head, food_pos, snake_body)
            self.current_path = self.wall_follower.current_path
        else:  # hamiltonian
            move = self.hamiltonian.get_next_move(snake_head, food_pos, snake_body)
            self.current_path = self.hamiltonian.current_path
        
        # Verify move safety
        dx, dy = move
        next_pos = (snake_head[0] + dx, snake_head[1] + dy)
        
        if not self.is_move_safe(next_pos, snake_body):
            # If chosen move isn't safe, try to find any safe move
            # Prioritize moves that get us closer to food
            possible_moves = []
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pos = (snake_head[0] + dx, snake_head[1] + dy)
                if self.is_move_safe(next_pos, snake_body):
                    distance_to_food = self.manhattan_distance(next_pos, food_pos)
                    possible_moves.append((distance_to_food, (dx, dy)))
            
            if possible_moves:
                # Choose the move that gets us closest to food
                _, best_move = min(possible_moves)
                self.current_path = [best_move]
                return best_move
        
        return move