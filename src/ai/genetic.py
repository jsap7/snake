from typing import List, Tuple
import random
import numpy as np
from .base import BaseAI

class GeneticAI(BaseAI):
    def __init__(self, weights=None):
        super().__init__()
        self.name = "Genetic Algorithm"
        self.description = "Evolves behavior weights through generations"
        self.current_path = []
        
        # Initialize weights for different behaviors (DNA)
        if weights is None:
            self.weights = {
                'food_distance': random.uniform(-1, 1),    # Weight for distance to food
                'wall_distance': random.uniform(-1, 1),    # Weight for distance to walls
                'tail_distance': random.uniform(-1, 1),    # Weight for distance to own tail
                'space_freedom': random.uniform(-1, 1)     # Weight for available free space
            }
        else:
            self.weights = weights
        
        self.fitness = 0  # Track fitness for evolution
    
    def calculate_move_score(self, pos: Tuple[int, int], snake_head: Tuple[int, int], 
                           food_pos: Tuple[int, int], snake_body: List[Tuple[int, int]]) -> float:
        """Calculate a score for a potential move based on weighted factors"""
        
        # Distance to food (normalized)
        food_dist = abs(pos[0] - food_pos[0]) + abs(pos[1] - food_pos[1])
        food_score = -food_dist / (self.grid_size * 2)  # Negative because shorter distance is better
        
        # Distance to walls (normalized)
        wall_dist = min(pos[0], pos[1], self.grid_size - 1 - pos[0], self.grid_size - 1 - pos[1])
        wall_score = wall_dist / self.grid_size
        
        # Distance to tail (normalized)
        tail_distances = [abs(pos[0] - x) + abs(pos[1] - y) for x, y in snake_body[1:]]
        tail_score = min(tail_distances) / (self.grid_size * 2) if tail_distances else 1.0
        
        # Available space (count free neighbors)
        free_neighbors = len(self.get_valid_neighbors(pos, snake_body))
        space_score = free_neighbors / 4  # Normalized by max possible neighbors
        
        # Combine scores using weights
        total_score = (
            self.weights['food_distance'] * food_score +
            self.weights['wall_distance'] * wall_score +
            self.weights['tail_distance'] * tail_score +
            self.weights['space_freedom'] * space_score
        )
        
        return total_score
    
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], 
                     snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        # Get valid neighboring positions
        neighbors = self.get_valid_neighbors(snake_head, snake_body)
        
        if not neighbors:
            return (0, 0)  # No valid moves
        
        # Score each possible move
        move_scores = []
        for pos in neighbors:
            score = self.calculate_move_score(pos, snake_head, food_pos, snake_body)
            move_scores.append((score, pos))
        
        # Choose the best move
        best_score, best_pos = max(move_scores)
        
        # Update current_path for visualization
        self.current_path = [best_pos]
        
        # Return direction to move
        return (best_pos[0] - snake_head[0], best_pos[1] - snake_head[1])
    
    def update_fitness(self, score: int, moves: int):
        """Update fitness based on game performance"""
        # Fitness considers both score and efficiency
        self.fitness = score * 100 + moves
    
    @staticmethod
    def crossover(parent1: 'GeneticAI', parent2: 'GeneticAI') -> 'GeneticAI':
        """Create a child by combining two parents' weights"""
        child_weights = {}
        for key in parent1.weights:
            # Randomly choose weights from either parent
            if random.random() < 0.5:
                child_weights[key] = parent1.weights[key]
            else:
                child_weights[key] = parent2.weights[key]
        
        # Add small random mutations
        for key in child_weights:
            if random.random() < 0.1:  # 10% mutation chance
                child_weights[key] += random.uniform(-0.2, 0.2)
                child_weights[key] = max(-1, min(1, child_weights[key]))  # Clamp to [-1, 1]
        
        return GeneticAI(weights=child_weights) 