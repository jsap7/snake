import random
from typing import List, Dict
from .genetic import GeneticAI

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