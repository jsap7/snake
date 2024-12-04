from src.ai.base import BaseAI
from typing import List, Tuple, Set
import random
from src.utils.settings import GRID_SIZE

class AdvancedHamiltonianAI(BaseAI):
    def __init__(self):
        super().__init__("advanced_hamiltonian")
        self.cycle = None
        self.cycle_map = {}  # Maps positions to their index in cycle
        self.grid_size = GRID_SIZE
        self.current_path = []  # For visualization
    
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Initialize cycle if not already done
        if not self.cycle:
            self.cycle = self._generate_hamiltonian_cycle()
            self.cycle_map = {pos: i for i, pos in enumerate(self.cycle)}
        
        # Check if positions are in cycle_map, if not regenerate cycle
        if snake_head not in self.cycle_map or food_pos not in self.cycle_map:
            self.cycle = self._generate_hamiltonian_cycle()
            self.cycle_map = {pos: i for i, pos in enumerate(self.cycle)}
        
        head = snake_head
        head_idx = self.cycle_map[head]
        food_idx = self.cycle_map[food_pos]
        
        # Check if we can safely take shortcuts
        valid_neighbors = self.get_valid_neighbors(snake_head, snake_body)
        best_move = None
        best_score = float('inf')
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (head[0] + dx, head[1] + dy)
            if next_pos not in self.cycle_map or next_pos not in valid_neighbors:
                continue
                
            next_idx = self.cycle_map[next_pos]
            
            # Score the move based on distance to food and safety
            if self._is_shortcut_safe(snake_head, next_pos, food_idx):
                # Calculate how much closer this move gets us to the food
                current_dist = (food_idx - head_idx) % len(self.cycle)
                new_dist = (food_idx - next_idx) % len(self.cycle)
                score = new_dist
                
                # Prefer moves that get us closer to food
                if score < best_score:
                    best_score = score
                    best_move = (dx, dy)
        
        # If no safe shortcut found, follow the cycle
        if not best_move:
            next_cycle_pos = self.cycle[(head_idx + 1) % len(self.cycle)]
            best_move = (next_cycle_pos[0] - head[0], next_cycle_pos[1] - head[1])
        
        # Update visualization path
        next_pos = (head[0] + best_move[0], head[1] + best_move[1])
        path_to_food = []
        current_pos = next_pos
        current_idx = self.cycle_map[current_pos]
        
        while current_idx != food_idx:
            path_to_food.append(current_pos)
            current_idx = (current_idx + 1) % len(self.cycle)
            current_pos = self.cycle[current_idx]
        path_to_food.append(food_pos)
        
        self.current_path = path_to_food
        return best_move
    
    def _is_shortcut_safe(self, snake_head: Tuple[int, int], next_pos: Tuple[int, int], food_idx: int) -> bool:
        # Check if taking this shortcut leaves enough space
        head_idx = self.cycle_map[snake_head]
        next_idx = self.cycle_map[next_pos]
        
        # Calculate the space we're skipping
        if next_idx < head_idx:
            next_idx += len(self.cycle)
        skipped_space = next_idx - head_idx - 1
        
        # Don't skip too much space if we're far from food
        max_skip = min(self.grid_size // 2, 10)
        if skipped_space > max_skip:
            return False
            
        return True
    
    def _generate_hamiltonian_cycle(self) -> List[Tuple[int, int]]:
        """Generates a Hamiltonian cycle using a modified Hierholzer's algorithm"""
        size = self.grid_size
        cycle = []
        
        # Start with a simple cycle along the edges
        for x in range(size):
            cycle.append((x, 0))
        for y in range(1, size):
            cycle.append((size-1, y))
        for x in range(size-2, -1, -1):
            cycle.append((x, size-1))
        for y in range(size-2, 0, -1):
            cycle.append((0, y))
            
        # Fill in the rest using a snake-like pattern
        for y in range(1, size-1):
            if y % 2 == 1:
                for x in range(1, size-1):
                    cycle.append((x, y))
            else:
                for x in range(size-2, 0, -1):
                    cycle.append((x, y))
        
        return cycle 