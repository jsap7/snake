from typing import List, Tuple, Set, Dict, Optional
from collections import deque
import heapq
from .base import BaseAI
from .astar import AStarAI
from .reverse_astar import ReverseAStarAI
from src.utils.settings import GRID_SIZE

class SmarterHybridAI(BaseAI):
    def __init__(self):
        super().__init__("smarter_hybrid")
        self.name = "Smarter Hybrid"
        self.description = "Enhanced A* with trap detection and Reverse A* backup"
        self.astar = AStarAI()
        self.reverse_astar = ReverseAStarAI()
        self.current_strategy = "astar"
        self.current_path = []
        self.last_positions = []
        self.stuck_count = 0
    
    def count_reachable_spaces(self, start_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> int:
        """Count how many spaces are reachable from a position"""
        visited = {start_pos}
        queue = deque([start_pos])
        
        while queue:
            current = queue.popleft()
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                next_pos = (current[0] + dx, current[1] + dy)
                if (0 <= next_pos[0] < GRID_SIZE and 
                    0 <= next_pos[1] < GRID_SIZE and 
                    next_pos not in snake_body and 
                    next_pos not in visited):
                    visited.add(next_pos)
                    queue.append(next_pos)
        
        return len(visited)
    
    def is_safe_move(self, move: Tuple[int, int], snake_head: Tuple[int, int], 
                     snake_body: List[Tuple[int, int]]) -> bool:
        """Check if a move is safe by ensuring it doesn't lead to a trap"""
        dx, dy = move
        next_pos = (snake_head[0] + dx, snake_head[1] + dy)
        
        # Basic boundary and collision checks
        if not (0 <= next_pos[0] < GRID_SIZE and 0 <= next_pos[1] < GRID_SIZE):
            return False
        if next_pos in snake_body[:-1]:
            return False
            
        # Simulate the move
        temp_body = snake_body[1:] + [next_pos]
        
        # Count immediate escape routes
        neighbors = self.get_valid_neighbors(next_pos, temp_body)
        if len(neighbors) == 0:
            return False
            
        # Check if we have enough space after the move
        # We need at least enough spaces for our body plus some buffer
        min_required_spaces = len(snake_body) + 2
        reachable_spaces = self.count_reachable_spaces(next_pos, temp_body)
        
        return reachable_spaces >= min_required_spaces
    
    def is_in_loop(self, snake_head: Tuple[int, int]) -> bool:
        """Detect if we're stuck in a small loop"""
        self.last_positions.append(snake_head)
        if len(self.last_positions) > 6:
            self.last_positions.pop(0)
            
        if len(self.last_positions) == 6:
            position_counts = {}
            for pos in self.last_positions:
                position_counts[pos] = position_counts.get(pos, 0) + 1
                if position_counts[pos] >= 3:  # Same position 3 times
                    return True
        return False
    
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], 
                      snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Try A* first
        self.astar.current_path = []
        astar_move = self.astar.get_next_move(snake_head, food_pos, snake_body)
        
        # If A* found a safe path, use it
        if astar_move != (0, 0) and self.is_safe_move(astar_move, snake_head, snake_body):
            self.current_strategy = "astar"
            self.current_path = self.astar.current_path
            self.stuck_count = 0
            return astar_move
        
        # If we're in a loop or A* failed, try Reverse A*
        if self.is_in_loop(snake_head) or astar_move == (0, 0):
            self.stuck_count += 1
            if self.stuck_count > 2:
                self.current_strategy = "reverse"
                reverse_move = self.reverse_astar.get_next_move(snake_head, food_pos, snake_body)
                if reverse_move != (0, 0) and self.is_safe_move(reverse_move, snake_head, snake_body):
                    self.current_path = self.reverse_astar.current_path
                    self.stuck_count = 0
                    return reverse_move
        
        # If both strategies fail, find any safe move
        # First try moves away from walls
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        safe_moves = []
        
        # Try each move and rank by available space
        for move in moves:
            if self.is_safe_move(move, snake_head, snake_body):
                dx, dy = move
                next_pos = (snake_head[0] + dx, snake_head[1] + dy)
                temp_body = snake_body[1:] + [next_pos]
                space_count = self.count_reachable_spaces(next_pos, temp_body)
                # Prefer moves that give us more space
                safe_moves.append((space_count, move))
        
        if safe_moves:
            # Choose the move that gives us the most space
            safe_moves.sort(reverse=True)
            _, best_move = safe_moves[0]
            return best_move
            
        # If no safe moves found, try to find any move that doesn't kill us immediately
        for move in moves:
            dx, dy = move
            next_pos = (snake_head[0] + dx, snake_head[1] + dy)
            if (0 <= next_pos[0] < GRID_SIZE and 
                0 <= next_pos[1] < GRID_SIZE and 
                next_pos not in snake_body[:-1]):
                neighbors = self.get_valid_neighbors(next_pos, snake_body[1:] + [next_pos])
                if neighbors:  # If there's at least one escape route
                    return move
                    
        return (0, 0)  # No valid moves found