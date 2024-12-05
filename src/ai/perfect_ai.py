from typing import List, Tuple
from .base import BaseAI
from .astar import AStarAI
from .hamiltonian import HamiltonianWithShortcutsAI
from src.utils.settings import GRID_SIZE

class PerfectAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "Perfect AI"
        self.description = "Combines A* with Hamiltonian cycle and safe shortcuts"
        self.astar = AStarAI()
        self.hamiltonian = HamiltonianWithShortcutsAI()
        self.current_strategy = "astar"
        self.current_path = []

    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        snake_length = len(snake_body)
        grid_area = GRID_SIZE * GRID_SIZE

        # Use A* when snake is short, switch to Hamiltonian with shortcuts when longer
        if snake_length < grid_area * 0.5:
            self.current_strategy = "astar"
            move = self.astar.get_next_move(snake_head, food_pos, snake_body)
            self.current_path = self.astar.current_path
        else:
            self.current_strategy = "hamiltonian"
            move = self.hamiltonian.get_next_move(snake_head, food_pos, snake_body)
            self.current_path = self.hamiltonian.current_path

        return move 