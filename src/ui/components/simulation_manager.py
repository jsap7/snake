import logging
import numpy as np
import queue
import traceback
from src.game.game import Game
import os

class SimulationManager:
    def __init__(self, root, algorithms, num_simulations):
        self.root = root
        self.algorithms = algorithms
        self.num_simulations = num_simulations
        self.result_queue = queue.Queue()
        self.simulation_results = {}
    
    def run_simulation(self, progress_callback):
        """
        Run simulations for all algorithms
        progress_callback: function to call with progress updates (0-100)
        """
        try:
            logging.info(f"Starting simulation thread with {len(self.algorithms)} algorithms, {self.num_simulations} runs each")
            total_sims = len(self.algorithms) * self.num_simulations
            completed_sims = 0
            
            # Initialize results dictionary with default values
            for algo_name, _, _ in self.algorithms:
                self.simulation_results[algo_name] = {
                    'scores': [],
                    'avg': 0,
                    'max': 0,
                    'std': 0,
                    'failed_runs': 0
                }
            
            # Report initial progress
            progress_callback(0)
            
            for algo_idx, (algo_name, algo_id, _) in enumerate(self.algorithms):
                logging.info(f"Starting simulations for algorithm: {algo_id} ({algo_idx + 1}/{len(self.algorithms)})")
                
                # Get the existing results dictionary
                results = self.simulation_results[algo_name]
                failed_runs = 0
                
                for i in range(self.num_simulations):
                    try:
                        # Create game instance with fast simulation settings
                        game_settings = {
                            'start_with_ai': True,
                            'ai_algorithm': algo_id,
                            'headless': True,
                            'max_steps_multiplier': 5
                        }
                        
                        # Adjust settings for specific algorithms
                        if algo_id in ['reverse_astar', 'advanced_hamiltonian', 'perfect']:
                            game_settings['max_steps_multiplier'] = 10
                        
                        game = Game(**game_settings)
                        score = game.run_headless()  # This will use fast simulation
                        
                        if score > 0:  # Only count non-zero scores
                            results['scores'].append(score)
                        else:
                            failed_runs += 1
                        
                        completed_sims += 1
                        # Update progress every 10 simulations or at the end
                        if completed_sims % 10 == 0 or completed_sims == total_sims:
                            progress = (completed_sims / total_sims) * 100
                            progress_callback(progress)
                        
                    except Exception as e:
                        logging.error(f"Error in simulation {i+1} for {algo_id}: {str(e)}")
                        logging.error(traceback.format_exc())
                        failed_runs += 1
                        completed_sims += 1
                        continue
                
                # Update results for this algorithm
                if results['scores']:
                    results.update({
                        'avg': float(np.mean(results['scores'])),
                        'max': float(np.max(results['scores'])),
                        'std': float(np.std(results['scores'])),
                        'failed_runs': failed_runs
                    })
                else:
                    # If no successful runs, keep default values and update failed runs
                    results['failed_runs'] = self.num_simulations
                
                logging.info(f"Completed algorithm {algo_id}: {results}")
            
            if not any(results['scores'] for results in self.simulation_results.values()):
                raise Exception("No successful simulations completed")
                
            logging.info("All simulations completed successfully")
            # Ensure we show 100% at the end
            progress_callback(100)
            return ("success", self.simulation_results)
            
        except Exception as e:
            logging.error(f"Critical simulation error: {str(e)}")
            logging.error(traceback.format_exc())
            # Ensure we show progress even on error
            progress_callback(100)
            return ("error", str(e)) 