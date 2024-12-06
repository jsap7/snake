import logging
import traceback
from src.ai.genetic_population import GeneticPopulation
from src.game.game import Game
import json
import os
from datetime import datetime

class TrainingManager:
    def __init__(self, population_size, generation_limit):
        self.population_size = population_size
        self.generation_limit = generation_limit
        self.genetic_population = None
        self.best_individual = None
        self.generation_stats = []
    
    def start_training(self, progress_callback):
        """
        Run genetic algorithm training
        progress_callback: function to call with progress updates (0-100)
        """
        try:
            self.genetic_population = GeneticPopulation(population_size=self.population_size)
            
            for generation in range(self.generation_limit):
                # Train each individual in the population
                for i in range(self.genetic_population.population_size):
                    individual = self.genetic_population.population[i]
                    game = Game(
                        start_with_ai=True,
                        ai_algorithm="genetic",
                        speed=30,
                        headless=True,
                        genetic_individual=individual
                    )
                    score = game.run_headless()
                    individual.update_fitness(score, game.moves)
                
                # Evolve population
                self.genetic_population.evolve()
                
                # Update progress
                progress = ((generation + 1) / self.generation_limit) * 100
                progress_callback(progress)
                
                # Store generation info
                info = self.genetic_population.get_generation_info()
                self.generation_stats.append(info)
                logging.info(f"Generation {info['generation']}: Best Fitness = {info['best_fitness_ever']}")
            
            self.best_individual = self.genetic_population.best_individual
            return ("success", self.generation_stats)
            
        except Exception as e:
            logging.error(f"Training error: {str(e)}")
            logging.error(traceback.format_exc())
            return ("error", str(e))
    
    def save_model(self):
        """Save the trained model"""
        if not self.best_individual:
            return None
            
        if not os.path.exists('trained_models'):
            os.makedirs('trained_models')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = f"genetic_model_{timestamp}"
        model_path = f"trained_models/{model_name}.json"
        
        model_data = {
            'weights': self.best_individual.weights,
            'fitness': self.genetic_population.best_fitness,
            'generation': self.genetic_population.generation
        }
        
        with open(model_path, 'w') as f:
            json.dump(model_data, f, indent=4)
        
        return model_name, model_path 