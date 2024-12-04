from src.ai.base import BaseAI
from src.ai.astar import AStarAI
from src.ai.advanced_hamiltonian import AdvancedHamiltonianAI
from typing import Tuple, List
from src.utils.settings import GRID_SIZE

class HybridAI(BaseAI):
    def __init__(self):
        super().__init__("hybrid")
        self.astar = AStarAI()
        self.hamiltonian = AdvancedHamiltonianAI()
        self.current_strategy = "astar"
        self.grid_size = GRID_SIZE
    
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Use A* when snake is short, switch to Hamiltonian when longer
        snake_length = len(snake_body)
        grid_area = self.grid_size ** 2
        
        # Dynamically switch strategies based on snake length
        if snake_length < grid_area * 0.5:
            self.current_strategy = "astar"
            move = self.astar.get_next_move(snake_head, food_pos, snake_body)
            # Get the current path from A*
            self.current_path = self.astar.current_path
            return move
        else:
            self.current_strategy = "hamiltonian"
            move = self.hamiltonian.get_next_move(snake_head, food_pos, snake_body)
            # Get the current path from Hamiltonian
            self.current_path = self.hamiltonian.current_path
            return move 