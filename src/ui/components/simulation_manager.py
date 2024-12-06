import logging
import numpy as np
import queue
import traceback
from src.game.game import Game

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
            logging.info("Simulation thread started")
            total_sims = len(self.algorithms) * self.num_simulations
            completed_sims = 0
            
            for algo_name, algo_id, _ in self.algorithms:
                logging.info(f"Starting simulations for algorithm: {algo_id}")
                scores = []
                
                for i in range(self.num_simulations):
                    logging.debug(f"Running simulation {i+1} for {algo_id}")
                    try:
                        game = Game(
                            start_with_ai=True,
                            ai_algorithm=algo_id,
                            speed=10,
                            headless=True,
                            max_steps_multiplier=3
                        )
                        score = game.run_headless()
                        scores.append(score)
                        
                        completed_sims += 1
                        if completed_sims % 5 == 0 or completed_sims == total_sims:
                            progress = (completed_sims / total_sims) * 100
                            progress_callback(progress)
                        
                    except Exception as e:
                        logging.error(f"Error in simulation {i+1} for {algo_id}: {str(e)}")
                        logging.error(traceback.format_exc())
                        continue
                
                if scores:
                    self.simulation_results[algo_name] = {
                        'scores': scores,
                        'avg': np.mean(scores),
                        'max': np.max(scores),
                        'std': np.std(scores)
                    }
                    logging.info(f"Results for {algo_id}: Avg={np.mean(scores):.2f}, Max={np.max(scores)}")
            
            logging.info("All simulations completed successfully")
            return ("success", self.simulation_results)
            
        except Exception as e:
            logging.error(f"Critical simulation error: {str(e)}")
            logging.error(traceback.format_exc())
            return ("error", str(e)) 