from typing import List, Tuple
from src.utils.settings import GRID_SIZE
from .base import BaseAI

class HamiltonianWithShortcutsAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "Hamiltonian + Shortcuts"
        self.description = "Follows Hamiltonian cycle with safe shortcuts"
        self._generate_cycle()
        self.current_path = []
    
    def _generate_cycle(self):
        """Generate a simple Hamiltonian cycle for the grid"""
        self.cycle = []
        # Start from top-left, go right, then snake down
        for y in range(GRID_SIZE):
            row = range(GRID_SIZE) if y % 2 == 0 else range(GRID_SIZE-1, -1, -1)
            for x in row:
                self.cycle.append((x, y))
        # Connect back to start
        self.cycle.append((0, 0))
    
    def _find_shortcut(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Try to find a safe shortcut to the food"""
        current_idx = self.cycle.index(snake_head)
        food_idx = self.cycle.index(food_pos)
        
        # Check if we can safely move directly towards food
        neighbors = self.get_valid_neighbors(snake_head, snake_body)
        for next_pos in neighbors:
            if next_pos not in self.cycle:
                continue
            next_idx = self.cycle.index(next_pos)
            
            # Only take shortcut if it's safe and gets us closer to food
            if (food_idx > current_idx and next_idx > current_idx) or \
               (food_idx < current_idx and next_idx < current_idx):
                return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        
        # No safe shortcut found, follow cycle
        next_pos = self.cycle[(current_idx + 1) % len(self.cycle)]
        return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])

    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Update current path for visualization
        current_idx = self.cycle.index(snake_head)
        self.current_path = []
        
        # Only take shortcuts when snake is small enough
        if len(snake_body) < GRID_SIZE * GRID_SIZE // 2:
            # Look ahead a few steps to show planned path
            next_pos = snake_head
            for _ in range(min(5, GRID_SIZE)):
                direction = self._find_shortcut(next_pos, food_pos, snake_body)
                next_pos = (next_pos[0] + direction[0], next_pos[1] + direction[1])
                self.current_path.append(next_pos)
            return self._find_shortcut(snake_head, food_pos, snake_body)
        else:
            # Show the next few steps of the Hamiltonian cycle
            for i in range(1, min(6, len(self.cycle))):
                self.current_path.append(self.cycle[(current_idx + i) % len(self.cycle)])
            next_pos = self.cycle[(current_idx + 1) % len(self.cycle)]
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1]) 