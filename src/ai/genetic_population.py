import random
from typing import List, Dict, Tuple
from .genetic import GeneticAI
from src.ai.base import BaseAI

class GeneticIndividual(BaseAI):
    def __init__(self):
        super().__init__()
        self.name = "Genetic Individual"
        self.description = "Trained genetic algorithm"
        self.weights = {
            'food_distance': random.uniform(-1, 1),
            'wall_distance': random.uniform(-1, 1),
            'tail_distance': random.uniform(-1, 1),
            'space_freedom': random.uniform(-1, 1)
        }
        self.fitness = 0
        self.current_path = []  # For visualization
    
    def calculate_features(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], 
                         snake_body: List[Tuple[int, int]]) -> Dict[str, float]:
        """Calculate input features for decision making"""
        # Distance to food
        food_distance = abs(snake_head[0] - food_pos[0]) + abs(snake_head[1] - food_pos[1])
        food_distance = 1.0 - (food_distance / (self.grid_size * 2))  # Normalize
        
        # Distance to walls
        wall_distance = min(
            snake_head[0],  # Distance to left wall
            self.grid_size - 1 - snake_head[0],  # Distance to right wall
            snake_head[1],  # Distance to top wall
            self.grid_size - 1 - snake_head[1]   # Distance to bottom wall
        )
        wall_distance = wall_distance / (self.grid_size / 2)  # Normalize
        
        # Distance to tail
        tail_distances = [abs(snake_head[0] - x) + abs(snake_head[1] - y) 
                        for x, y in snake_body[1:]]
        tail_distance = min(tail_distances) if tail_distances else self.grid_size
        tail_distance = tail_distance / self.grid_size  # Normalize
        
        # Available space (freedom of movement)
        neighbors = self.get_valid_neighbors(snake_head, snake_body)
        space_freedom = len(neighbors) / 4  # Normalize by max possible neighbors
        
        return {
            'food_distance': food_distance,
            'wall_distance': wall_distance,
            'tail_distance': tail_distance,
            'space_freedom': space_freedom
        }
    
    def get_next_move(self, snake_head: Tuple[int, int], food_pos: Tuple[int, int], 
                      snake_body: List[Tuple[int, int]]) -> Tuple[int, int]:
        """Decide next move based on current state and learned weights"""
        # Get all possible moves
        possible_moves = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (snake_head[0] + dx, snake_head[1] + dy)
            if new_pos not in snake_body and 0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size:
                possible_moves.append((dx, dy, new_pos))
        
        if not possible_moves:
            return (0, 0)
        
        # Evaluate each move
        best_move = None
        best_score = float('-inf')
        
        for dx, dy, new_pos in possible_moves:
            # Calculate features for this move
            features = self.calculate_features(new_pos, food_pos, snake_body)
            
            # Calculate weighted sum
            score = sum(self.weights[feature] * value 
                       for feature, value in features.items())
            
            if score > best_score:
                best_score = score
                best_move = (dx, dy)
                self.current_path = [new_pos]  # Update visualization path
        
        return best_move or (0, 0)
    
    def update_fitness(self, score: int, moves: int):
        """Update individual's fitness based on game performance"""
        # Reward higher scores and penalize excessive moves
        self.fitness = score * 100 - moves
        if self.fitness < 0:
            self.fitness = 0

class GeneticPopulation:
    def __init__(self, population_size: int = 50):
        self.population_size = population_size
        self.generation = 0
        self.population: List[GeneticAI] = []
        self.best_individual: GeneticAI = None
        self.best_fitness = 0
        self.generation_stats: List[Dict] = []
        
        # Initialize population
        self.initialize_population()
    
    def initialize_population(self):
        """Create initial population with random weights"""
        self.population = [GeneticAI() for _ in range(self.population_size)]
    
    def evolve(self):
        """Evolve the population to create the next generation"""
        # Sort population by fitness
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Update best individual
        if self.population[0].fitness > self.best_fitness:
            self.best_fitness = self.population[0].fitness
            self.best_individual = GeneticAI(weights=self.population[0].weights.copy())
        
        # Record generation statistics
        self.generation_stats.append({
            'generation': self.generation,
            'best_fitness': self.population[0].fitness,
            'avg_fitness': sum(x.fitness for x in self.population) / len(self.population)
        })
        
        # Select top performers (top 20%)
        elite_size = max(2, self.population_size // 5)
        elite = self.population[:elite_size]
        
        # Create new population
        new_population = []
        
        # Keep elite individuals
        new_population.extend(GeneticAI(weights=x.weights.copy()) for x in elite)
        
        # Fill rest with children
        while len(new_population) < self.population_size:
            # Select parents (tournament selection)
            parent1 = self.tournament_select()
            parent2 = self.tournament_select()
            
            # Create child
            child = GeneticAI.crossover(parent1, parent2)
            new_population.append(child)
        
        self.population = new_population
        self.generation += 1
    
    def tournament_select(self, tournament_size: int = 3) -> GeneticAI:
        """Select an individual using tournament selection"""
        tournament = random.sample(self.population, tournament_size)
        return max(tournament, key=lambda x: x.fitness)
    
    def get_current_individual(self) -> GeneticAI:
        """Get the current individual being evaluated"""
        if not self.population:
            self.initialize_population()
        return self.population[0]
    
    def update_current_fitness(self, score: int, moves: int):
        """Update the fitness of the current individual"""
        if self.population:
            self.population[0].update_fitness(score, moves)
    
    def get_generation_info(self) -> Dict:
        """Get information about the current generation"""
        return {
            'generation': self.generation,
            'population_size': self.population_size,
            'best_fitness_ever': self.best_fitness,
            'current_best_fitness': max(x.fitness for x in self.population) if self.population else 0
        } 