from typing import List, Tuple, Set, Dict, Optional
from .base import BaseAI
from collections import deque
import logging

class DFSAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "DFS Exploration"
        self.description = "Depth-first search for shortest path"
        self.current_path = []
        self.visited: Set[Tuple[int, int]] = set()

    def dfs(self, start: Tuple[int, int], goal: Tuple[int, int], snake_body: List[Tuple[int, int]], max_depth: int = 30) -> Optional[List[Tuple[int, int]]]:
        """Perform DFS to find path to food"""
        stack = [(start, [start])]
        visited = set([start])  # Only mark cells we've actually visited
        snake_set = set(snake_body)  # Convert snake body to set for faster lookups
        
        while stack:
            current, path = stack.pop()
            
            # If path is too long, skip this branch
            if len(path) > max_depth:
                continue
                
            if current == goal:
                logging.debug(f"DFS found path of length {len(path)}")
                return path
                
            # Get valid neighbors not in snake body
            neighbors = self.get_valid_neighbors(current, snake_body)
            # Sort neighbors by distance to goal for better paths
            neighbors.sort(key=lambda pos: abs(pos[0] - goal[0]) + abs(pos[1] - goal[1]))
            
            for next_pos in neighbors:
                if next_pos not in visited and next_pos not in snake_set:
                    visited.add(next_pos)
                    stack.append((next_pos, path + [next_pos]))
        
        logging.debug("DFS found no path to food")
        return None

    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Try to find path to food
        path = self.dfs(snake_head, food_pos, snake_body)
        
        if path and len(path) > 1:
            # Found path to food, use it
            self.current_path = path[1:]  # Exclude snake head
            next_pos = path[1]
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        
        # If no path to food, explore safely
        neighbors = self.get_valid_neighbors(snake_head, snake_body)
        if neighbors:
            # Sort neighbors by distance to food
            neighbors.sort(key=lambda pos: abs(pos[0] - food_pos[0]) + abs(pos[1] - food_pos[1]))
            next_pos = neighbors[0]  # Take the move closest to food
            self.current_path = [next_pos]
            return (next_pos[0] - snake_head[0], next_pos[1] - snake_head[1])
        
        return (0, 0)  # No valid moves

    def reset(self):
        """Reset the visited set when starting a new game"""
        self.visited.clear()
        self.current_path = []