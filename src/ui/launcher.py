import customtkinter as ctk
from src.game.game import Game
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import json
from datetime import datetime
import os
import logging
import traceback
import queue
import threading
from src.ai.genetic_population import GeneticPopulation

# Configure logging - disable matplotlib font debugging
logging.getLogger('matplotlib.font_manager').disabled = True
logging.basicConfig(
    level=logging.INFO,  # Change to INFO level
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simulation.log'),
    ]
)
# Disable matplotlib font debugging
logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)

class GameLauncher:
    def __init__(self):
        logging.info("Initializing GameLauncher")
        self.result_queue = queue.Queue()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("Snake Game Launcher")
        self.root.geometry("1300x700")
        self.root.resizable(False, False)
        
        # Variables
        self.control_mode = ctk.StringVar(value="human")
        self.algorithm = ctk.StringVar(value="astar")
        self.speed = ctk.IntVar(value=10)
        self.num_simulations = ctk.IntVar(value=10)
        self.simulation_results = {}
        
        # Genetic Algorithm variables
        self.genetic_population = None
        self.population_size = ctk.IntVar(value=50)
        self.generation_limit = ctk.IntVar(value=20)
        
        # Store algorithms list as class variable
        self.algorithms = [
            ("🎯 A* Pathfinding", "astar", "Optimal path finding to food"),
            ("🌊 BFS Pathfinding", "bfs", "Breadth-first search for shortest path"),
            ("🔄 Advanced Hamiltonian", "advanced_hamiltonian", "Optimized safe path"),
            ("🤖 Hybrid A*/Hamiltonian", "hybrid", "Adaptive strategy switching"),
            ("🔍 DFS Exploration", "dfs", "Depth-first exploration"),
            ("🎲 Random Walk", "random", "Random valid moves"),
            ("⚡ Greedy Best-First", "greedy", "Always moves towards food"),
            ("🌐 Dijkstra", "dijkstra", "Finds shortest path by exploring all directions"),
            ("🧱 Wall Follower", "wall_follower", "Follows walls and edges of the grid"),
            ("🎮 Smart Hybrid", "smart_hybrid", "Combines A* and Wall Following adaptively"),
            ("🧬 Genetic Algorithm", "genetic", "Evolves behavior through generations")
        ]
        
        self.create_widgets()
        logging.info("GameLauncher initialized successfully")
    
    def create_widgets(self):
        # Main container
        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="🐍 Snake Game",
            font=ctk.CTkFont(size=32, weight="bold"),
        )
        title_label.pack(pady=(0, 20))
        
        # Create two columns
        columns_frame = ctk.CTkFrame(container)
        columns_frame.pack(fill="both", expand=True, padx=10)
        
        # Left Column
        left_column = ctk.CTkFrame(columns_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Game Mode Frame
        mode_frame = ctk.CTkFrame(left_column)
        mode_frame.pack(fill="x", pady=(0, 20))
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="Game Mode",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        mode_label.pack(pady=(10, 5))
        
        # Mode Selection with Training
        mode_buttons_frame = ctk.CTkFrame(mode_frame)
        mode_buttons_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkRadioButton(
            mode_buttons_frame,
            text="👤 Human",
            variable=self.control_mode,
            value="human",
            command=self.toggle_options,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=20)
        
        ctk.CTkRadioButton(
            mode_buttons_frame,
            text="🤖 AI",
            variable=self.control_mode,
            value="ai",
            command=self.toggle_options,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=20)
        
        ctk.CTkRadioButton(
            mode_buttons_frame,
            text="📊 Simulation",
            variable=self.control_mode,
            value="simulation",
            command=self.toggle_options,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=20)
        
        ctk.CTkRadioButton(
            mode_buttons_frame,
            text="🧬 Training",
            variable=self.control_mode,
            value="training",
            command=self.toggle_options,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=20)
        
        # Game Speed Frame
        self.speed_frame = ctk.CTkFrame(left_column)
        self.speed_frame.pack(fill="x", pady=(0, 20))
        
        speed_label = ctk.CTkLabel(
            self.speed_frame,
            text="Game Speed",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        speed_label.pack(pady=(10, 5))
        
        speed_slider_frame = ctk.CTkFrame(self.speed_frame)
        speed_slider_frame.pack(fill="x", padx=20, pady=10)
        
        self.fps_label = ctk.CTkLabel(
            speed_slider_frame,
            text="10 FPS",
            font=ctk.CTkFont(size=14)
        )
        self.fps_label.pack(side="right", padx=10)
        
        speed_slider = ctk.CTkSlider(
            speed_slider_frame,
            from_=5,
            to=30,
            variable=self.speed,
            command=self.update_speed_label
        )
        speed_slider.pack(fill="x", padx=(10, 10))
        
        # Simulation Settings Frame
        self.sim_frame = ctk.CTkFrame(left_column)
        self.sim_frame.pack(fill="x", pady=(0, 20))
        
        sim_label = ctk.CTkLabel(
            self.sim_frame,
            text="Simulation Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        sim_label.pack(pady=(10, 5))
        
        sim_count_frame = ctk.CTkFrame(self.sim_frame)
        sim_count_frame.pack(fill="x", padx=20, pady=10)
        
        self.sim_count_label = ctk.CTkLabel(
            sim_count_frame,
            text="10 games per AI",
            font=ctk.CTkFont(size=14)
        )
        self.sim_count_label.pack(side="right", padx=10)
        
        sim_slider = ctk.CTkSlider(
            sim_count_frame,
            from_=5,
            to=100,
            variable=self.num_simulations,
            command=self.update_sim_label
        )
        sim_slider.pack(fill="x", padx=(10, 10))
        
        # Training Settings Frame
        self.training_frame = ctk.CTkFrame(left_column)
        self.training_frame.pack(fill="x", pady=(0, 20))
        
        training_label = ctk.CTkLabel(
            self.training_frame,
            text="Training Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        training_label.pack(pady=(10, 5))
        
        # Population Size
        pop_frame = ctk.CTkFrame(self.training_frame)
        pop_frame.pack(fill="x", padx=20, pady=5)
        
        self.pop_label = ctk.CTkLabel(
            pop_frame,
            text="Population: 50",
            font=ctk.CTkFont(size=14)
        )
        self.pop_label.pack(side="right", padx=10)
        
        pop_slider = ctk.CTkSlider(
            pop_frame,
            from_=10,
            to=100,
            variable=self.population_size,
            command=self.update_pop_label
        )
        pop_slider.pack(fill="x", padx=(10, 10))
        
        # Generation Limit
        gen_frame = ctk.CTkFrame(self.training_frame)
        gen_frame.pack(fill="x", padx=20, pady=5)
        
        self.gen_label = ctk.CTkLabel(
            gen_frame,
            text="Generations: 20",
            font=ctk.CTkFont(size=14)
        )
        self.gen_label.pack(side="right", padx=10)
        
        gen_slider = ctk.CTkSlider(
            gen_frame,
            from_=5,
            to=50,
            variable=self.generation_limit,
            command=self.update_gen_label
        )
        gen_slider.pack(fill="x", padx=(10, 10))
        
        # Right Column - AI Algorithms
        right_column = ctk.CTkFrame(columns_frame)
        right_column.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        algorithms_label = ctk.CTkLabel(
            right_column,
            text="AI Algorithm",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        algorithms_label.pack(pady=(10, 5))
        
        # Scrollable frame for algorithms - increase width and adjust wraplength
        algorithms_scroll = ctk.CTkScrollableFrame(
            right_column,
            height=350,
            width=600  # Increased width
        )
        algorithms_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.radio_buttons = []
        
        for text, value, desc in self.algorithms:
            frame = ctk.CTkFrame(algorithms_scroll)
            frame.pack(fill="x", pady=5)
            
            radio = ctk.CTkRadioButton(
                frame,
                text=text,
                variable=self.algorithm,
                value=value,
                font=ctk.CTkFont(size=14),
                width=200  # Fixed width for radio buttons
            )
            radio.pack(side="left", padx=10)
            
            desc_label = ctk.CTkLabel(
                frame,
                text=desc,
                font=ctk.CTkFont(size=12),
                wraplength=350,  # Increased wraplength
                justify="left"   # Ensure left alignment
            )
            desc_label.pack(side="left", padx=(5, 10), fill="x", expand=True)
        
        # Buttons Frame
        buttons_frame = ctk.CTkFrame(container)
        buttons_frame.pack(pady=20)
        
        # Game Button
        self.game_button = ctk.CTkButton(
            buttons_frame,
            text="▶  Start Game",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_game,
            width=200,
            height=40
        )
        self.game_button.pack(side="left", padx=10)
        
        # Training Button
        self.train_button = ctk.CTkButton(
            buttons_frame,
            text="🧬 Start Training",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_training,
            width=200,
            height=40,
            fg_color="#2B7821",  # Green color
            hover_color="#1F5817"
        )
        self.train_button.pack(side="left", padx=10)
        
        # Initial state
        self.toggle_options()
    
    def update_speed_label(self, value):
        self.fps_label.configure(text=f"{int(float(value))} FPS")
    
    def update_sim_label(self, value):
        self.sim_count_label.configure(text=f"{int(float(value))} games per AI")
    
    def update_pop_label(self, value):
        self.pop_label.configure(text=f"Population: {int(float(value))}")
    
    def update_gen_label(self, value):
        self.gen_label.configure(text=f"Generations: {int(float(value))}")
    
    def toggle_options(self):
        mode = self.control_mode.get()
        # Toggle AI options
        ai_state = "normal" if mode == "ai" else "disabled"
        for radio in self.radio_buttons:
            radio.configure(state=ai_state)
        
        # Toggle simulation settings
        sim_state = "normal" if mode == "simulation" else "disabled"
        for widget in self.sim_frame.winfo_children():
            if isinstance(widget, (ctk.CTkSlider, ctk.CTkLabel, ctk.CTkFrame)):
                try:
                    widget.configure(state=sim_state)
                except ValueError:
                    for child in widget.winfo_children():
                        child.configure(state=sim_state)
        
        # Toggle training settings
        train_state = "normal" if mode == "training" else "disabled"
        for widget in self.training_frame.winfo_children():
            if isinstance(widget, (ctk.CTkSlider, ctk.CTkLabel, ctk.CTkFrame)):
                try:
                    widget.configure(state=train_state)
                except ValueError:
                    for child in widget.winfo_children():
                        child.configure(state=train_state)
        
        # Toggle buttons
        self.game_button.configure(state="normal" if mode in ["human", "ai"] else "disabled")
        self.train_button.configure(state="normal" if mode == "training" else "disabled")
        
        # Add this line to handle simulation mode
        if mode == "simulation":
            self.start_simulation()
    
    def start_training(self):
        """Start genetic algorithm training"""
        from src.ai.genetic_population import GeneticPopulation
        
        self.genetic_population = GeneticPopulation(population_size=self.population_size.get())
        progress_window = self.create_progress_window(self.generation_limit.get())
        
        def train():
            try:
                for generation in range(self.generation_limit.get()):
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
                    progress = ((generation + 1) / self.generation_limit.get()) * 100
                    self.root.after(0, lambda p=progress: progress_window.update_progress(p))
                    
                    # Update generation info
                    info = self.genetic_population.get_generation_info()
                    logging.info(f"Generation {info['generation']}: Best Fitness = {info['best_fitness_ever']}")
                
                # Training complete
                self.root.after(0, lambda: [progress_window.destroy(), self.show_training_results()])
                
            except Exception as e:
                logging.error(f"Training error: {str(e)}")
                logging.error(traceback.format_exc())
                self.root.after(0, lambda: [progress_window.destroy(), self.show_error_dialog(str(e))])
            finally:
                self.root.after(0, self.enable_buttons)
        
        # Disable buttons during training
        self.game_button.configure(state="disabled")
        self.train_button.configure(state="disabled")
        
        # Start training thread
        train_thread = threading.Thread(target=train)
        train_thread.daemon = True
        train_thread.start()
    
    def show_training_results(self):
        """Show the results of genetic algorithm training"""
        results_window = ctk.CTkToplevel(self.root)
        results_window.title("Training Results")
        results_window.geometry("1000x800")
        
        # Create main container
        container = ctk.CTkFrame(results_window)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            container,
            text="🎮 Genetic Algorithm Training Results",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 30))
        
        # Create plots
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(14, 10))
        fig.patch.set_facecolor('#1E1E1E')
        
        # Plot fitness over generations
        generations = [stat['generation'] for stat in self.genetic_population.generation_stats]
        best_fitness = [stat['best_fitness'] for stat in self.genetic_population.generation_stats]
        avg_fitness = [stat['avg_fitness'] for stat in self.genetic_population.generation_stats]
        
        ax1 = plt.subplot(2, 1, 1)
        ax1.plot(generations, best_fitness, label='Best Fitness', color='#2ecc71')
        ax1.plot(generations, avg_fitness, label='Average Fitness', color='#3498db')
        ax1.set_title('Fitness Over Generations', color='white', pad=20)
        ax1.set_xlabel('Generation', color='white')
        ax1.set_ylabel('Fitness', color='white')
        ax1.legend()
        ax1.grid(True, alpha=0.2)
        
        # Plot best individual's weights
        best = self.genetic_population.best_individual
        if best:
            ax2 = plt.subplot(2, 1, 2)
            weights = list(best.weights.values())
            labels = list(best.weights.keys())
            x = np.arange(len(labels))
            ax2.bar(x, weights, color='#e74c3c')
            ax2.set_title('Best Individual Weights', color='white', pad=20)
            ax2.set_xticks(x)
            ax2.set_xticklabels(labels, rotation=45)
            ax2.grid(True, alpha=0.2)
        
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=(0, 20))
        
        # Save best individual button
        save_button = ctk.CTkButton(
            container,
            text="💾 Save Best Individual",
            font=ctk.CTkFont(size=14),
            command=self.save_best_individual,
            width=200,
            height=35
        )
        save_button.pack(pady=10)
    
    def save_best_individual(self):
        """Save the best individual's weights to a file"""
        if self.genetic_population and self.genetic_population.best_individual:
            if not os.path.exists('genetic_models'):
                os.makedirs('genetic_models')
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"genetic_models/best_individual_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    'weights': self.genetic_population.best_individual.weights,
                    'fitness': self.genetic_population.best_fitness,
                    'generation': self.genetic_population.generation
                }, f, indent=4)
            
            self.show_message("Success", f"Best individual saved to {filename}")
    
    def show_message(self, title, message):
        """Show a message dialog"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x200")
        
        label = ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=350
        )
        label.pack(pady=20, padx=20)
        
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        )
        ok_button.pack(pady=20)
    
    def start_game(self):
        self.root.withdraw()
        game = Game(
            start_with_ai=self.control_mode.get() == "ai",
            ai_algorithm=self.algorithm.get(),
            speed=self.speed.get()
        )
        game.run()
        self.root.deiconify()
    
    def start_simulation(self):
        import threading
        logging.info("Starting simulation process")
        
        def run_sim():
            try:
                logging.info("Simulation thread started")
                self.simulation_results = {}
                total_sims = len(self.algorithms) * self.num_simulations.get()
                logging.info(f"Planning to run {total_sims} total simulations")
                
                # Create progress window in main thread
                self.root.after(0, lambda: self.create_and_store_progress_window(total_sims))
                
                for algo_name, algo_id, _ in self.algorithms:
                    logging.info(f"Starting simulations for algorithm: {algo_id}")
                    scores = []
                    
                    for i in range(self.num_simulations.get()):
                        logging.debug(f"Running simulation {i+1} for {algo_id}")
                        try:
                            game = Game(
                                start_with_ai=True,
                                ai_algorithm=algo_id,
                                speed=30,
                                headless=True
                            )
                            score = game.run_headless()
                            scores.append(score)
                            
                            # Calculate progress
                            progress = ((len(scores) + (self.algorithms.index((algo_name, algo_id, _)) * 
                                       self.num_simulations.get())) / total_sims) * 100
                            
                            # Update progress in main thread
                            self.root.after(0, lambda p=progress: self.update_progress(p))
                            
                        except Exception as e:
                            logging.error(f"Error in simulation {i+1} for {algo_id}: {str(e)}")
                            logging.error(traceback.format_exc())
                            continue
                    
                    if scores:
                        self.simulation_results[algo_name] = {
                            'scores': scores,
                            'avg': np.mean(scores),
                            'max': np.max(scores)
                        }
                        logging.info(f"Results for {algo_id}: Avg={np.mean(scores):.2f}, Max={np.max(scores)}")
                
                logging.info("All simulations completed successfully")
                # Put results in queue for main thread to handle
                self.result_queue.put(("success", self.simulation_results))
                
            except Exception as e:
                logging.error(f"Critical simulation error: {str(e)}")
                logging.error(traceback.format_exc())
                self.result_queue.put(("error", str(e)))
        
        # Disable buttons during simulation
        self.train_button.configure(state="disabled")
        self.game_button.configure(state="disabled")
        
        # Start simulation thread
        sim_thread = threading.Thread(target=run_sim)
        sim_thread.daemon = True
        sim_thread.start()
        
        # Start checking for results
        self.root.after(100, self.check_simulation_results)
    
    def create_and_store_progress_window(self, total_sims):
        self.progress_window = SimulationProgress(self.root, total_sims)
    
    def update_progress(self, progress):
        if hasattr(self, 'progress_window'):
            self.progress_window.update_progress(progress)
    
    def check_simulation_results(self):
        try:
            result_type, result_data = self.result_queue.get_nowait()
            
            if hasattr(self, 'progress_window'):
                self.progress_window.destroy()
            
            if result_type == "success":
                self.simulation_results = result_data
                self.show_simulation_results()
            else:
                self.show_error_dialog(result_data)
            
            # Re-enable buttons
            self.train_button.configure(state="normal")
            self.game_button.configure(state="normal")
            
        except queue.Empty:
            # No result yet, check again in 100ms
            self.root.after(100, self.check_simulation_results)
    
    def show_error_dialog(self, error_message):
        logging.info("Showing error dialog")
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("Simulation Error")
        error_window.geometry("400x200")
        
        error_label = ctk.CTkLabel(
            error_window,
            text=f"An error occurred during simulation:\n\n{error_message}",
            wraplength=350
        )
        error_label.pack(pady=20, padx=20)
        
        ok_button = ctk.CTkButton(
            error_window,
            text="OK",
            command=error_window.destroy
        )
        ok_button.pack(pady=20)
    
    def show_simulation_results(self):
        results_window = ctk.CTkToplevel(self.root)
        results_window.title("Simulation Results")
        results_window.geometry("1400x900")
        
        # Create main container
        container = ctk.CTkFrame(results_window)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            container,
            text="🎮 AI Performance Analysis",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 30))
        
        # Create matplotlib figure with custom style
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(14, 10))
        fig.patch.set_facecolor('#1E1E1E')  # Slightly lighter than black
        
        # Custom colors
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f1c40f', '#9b59b6', 
                 '#1abc9c', '#e67e22', '#34495e', '#7f8c8d', '#c0392b']
        
        # Performance Comparison (Bar Chart)
        ax1 = plt.subplot2grid((2, 1), (0, 0))
        ax1.set_facecolor('#1E1E1E')
        
        # Clean up algorithm names (remove emojis)
        algorithms = list(self.simulation_results.keys())
        clean_names = [name.split(' ', 1)[1] for name in algorithms]  # Remove emoji prefix
        
        avg_scores = [self.simulation_results[algo]['avg'] for algo in algorithms]
        max_scores = [self.simulation_results[algo]['max'] for algo in algorithms]
        
        x = np.arange(len(clean_names))
        width = 0.35
        
        # Create bars with custom styling
        bars1 = ax1.bar(x - width/2, avg_scores, width, label='Average Score', 
                       color='#3498db', alpha=0.8)
        bars2 = ax1.bar(x + width/2, max_scores, width, label='Max Score',
                       color='#2ecc71', alpha=0.8)
        
        # Add value labels on top of bars
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax1.annotate(f'{int(height)}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom',
                           color='white', fontsize=8)
        
        autolabel(bars1)
        autolabel(bars2)
        
        # Customize first subplot
        ax1.set_title('Performance Comparison', color='white', pad=20, fontsize=16)
        ax1.set_xticks(x)
        ax1.set_xticklabels(clean_names, rotation=45, ha='right')
        # Move legend outside of the plot area
        ax1.legend(bbox_to_anchor=(1.02, 1), loc='upper left', framealpha=0.8)
        ax1.grid(True, alpha=0.2)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        
        # Algorithm Rankings (Bottom Plot)
        ax2 = plt.subplot2grid((2, 1), (1, 0))
        ax2.set_facecolor('#1E1E1E')
        
        # Calculate algorithm scores
        algorithm_scores = []
        for algo in algorithms:
            data = self.simulation_results[algo]
            avg_score = data['avg']
            max_score = data['max']
            consistency = 1 - (np.std(data['scores']) / max_score)  # Normalized consistency
            
            # Calculate overall score (weighted average of metrics)
            overall_score = (
                0.4 * (avg_score / max(avg_scores)) +  # Normalized average score (40% weight)
                0.4 * (max_score / max(max_scores)) +  # Normalized max score (40% weight)
                0.2 * consistency                      # Consistency score (20% weight)
            ) * 100  # Convert to percentage
            
            algorithm_scores.append({
                'name': clean_names[algorithms.index(algo)],
                'score': overall_score,
                'avg_score': avg_score,
                'max_score': max_score,
                'consistency': consistency * 100
            })
        
        # Sort algorithms by overall score
        algorithm_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Create ranking visualization
        names = [score['name'] for score in algorithm_scores]
        scores = [score['score'] for score in algorithm_scores]
        
        # Create horizontal bars for rankings
        bars = ax2.barh(np.arange(len(names)), scores, 
                       color=[colors[i % len(colors)] for i in range(len(names))],
                       alpha=0.8)
        
        # Add score labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width + 1, bar.get_y() + bar.get_height()/2,
                    f'{scores[i]:.1f}%',
                    va='center', color='white')
        
        # Customize ranking subplot
        ax2.set_title('Algorithm Rankings', color='white', pad=20, fontsize=16)
        ax2.set_yticks(np.arange(len(names)))
        ax2.set_yticklabels(names)
        ax2.set_xlim(0, 105)  # Leave room for percentage labels
        ax2.grid(True, alpha=0.2)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        
        # Add ranking criteria explanation
        criteria_text = "Ranking Criteria:\n" + \
                       "• 40% Average Score\n" + \
                       "• 40% Max Score\n" + \
                       "• 20% Consistency"
        
        props = dict(boxstyle='round', facecolor='#2C3E50', alpha=0.8)
        ax2.text(1.02, 0.02, criteria_text,
                transform=ax2.transAxes,
                fontsize=10,
                verticalalignment='bottom',
                bbox=props)
        
        # Adjust layout
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=(0, 20))
        
        # Save results button
        save_button = ctk.CTkButton(
            container,
            text="💾 Save Results",
            font=ctk.CTkFont(size=14),
            command=lambda: self.save_simulation_results(),
            width=150,
            height=35
        )
        save_button.pack(pady=10)
    
    def save_simulation_results(self):
        # Create results directory if it doesn't exist
        if not os.path.exists('simulation_results'):
            os.makedirs('simulation_results')
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"simulation_results/snake_simulation_{timestamp}.json"
        
        # Save results
        with open(filename, 'w') as f:
            json.dump(self.simulation_results, f, indent=4)
    
    def run(self):
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()

    def create_progress_window(self, total_generations):
        """Create a progress window for training"""
        class TrainingProgress(ctk.CTkToplevel):
            def __init__(self, parent, total):
                super().__init__(parent)
                self.title("Training Progress")
                self.geometry("400x150")
                
                # Center window
                self.update_idletasks()
                width = self.winfo_width()
                height = self.winfo_height()
                x = (self.winfo_screenwidth() // 2) - (width // 2)
                y = (self.winfo_screenheight() // 2) - (height // 2)
                self.geometry(f'{width}x{height}+{x}+{y}')
                
                self.total = total
                
                # Progress label
                self.label = ctk.CTkLabel(
                    self,
                    text="Training Generation 0/%d..." % total,
                    font=ctk.CTkFont(size=14)
                )
                self.label.pack(pady=20)
                
                # Progress bar
                self.progress_bar = ctk.CTkProgressBar(self)
                self.progress_bar.pack(pady=20, padx=20, fill="x")
                self.progress_bar.set(0)
            
            def update_progress(self, progress):
                """Update progress bar and label"""
                self.progress_bar.set(progress / 100)
                generation = int((progress / 100) * self.total)
                self.label.configure(text=f"Training Generation {generation}/{self.total}...")
                self.update()
        
        return TrainingProgress(self.root, total_generations)

    def enable_buttons(self):
        """Re-enable buttons after training/simulation"""
        self.game_button.configure(state="normal")
        self.train_button.configure(state="normal")

class SimulationProgress(ctk.CTkToplevel):
    def __init__(self, parent, total_sims):
        super().__init__(parent)
        self.title("Simulation Progress")
        self.geometry("300x150")
        
        self.label = ctk.CTkLabel(
            self,
            text="Running simulations...",
            font=ctk.CTkFont(size=14)
        )
        self.label.pack(pady=20)
        
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=20, padx=20, fill="x")
        self.progress_bar.set(0)
    
    def update_progress(self, progress):
        self.progress_bar.set(progress / 100)
        self.update()