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

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simulation.log'),
        logging.StreamHandler()
    ]
)

class GameLauncher:
    def __init__(self):
        logging.info("Initializing GameLauncher")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("Snake Game Launcher")
        self.root.geometry("1200x900")
        self.root.resizable(False, False)
        
        # Variables
        self.control_mode = ctk.StringVar(value="human")
        self.algorithm = ctk.StringVar(value="astar")
        self.speed = ctk.IntVar(value=10)
        self.num_simulations = ctk.IntVar(value=10)
        self.simulation_results = {}
        
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
            ("🎮 Smart Hybrid", "smart_hybrid", "Combines A* and Wall Following adaptively")
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
        
        # Mode Selection with Simulation
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
        
        # Simulation Button
        self.sim_button = ctk.CTkButton(
            buttons_frame,
            text="📊 Run Simulation",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_simulation,
            width=200,
            height=40,
            fg_color="#2B7821",  # Green color to distinguish
            hover_color="#1F5817"
        )
        self.sim_button.pack(side="left", padx=10)
        
        # Initial state
        self.toggle_options()
    
    def update_speed_label(self, value):
        self.fps_label.configure(text=f"{int(float(value))} FPS")
    
    def update_sim_label(self, value):
        self.sim_count_label.configure(text=f"{int(float(value))} games per AI")
    
    def toggle_options(self):
        mode = self.control_mode.get()
        # Toggle AI options
        ai_state = "normal" if mode == "ai" else "disabled"
        for radio in self.radio_buttons:
            radio.configure(state=ai_state)
        
        # Toggle simulation settings by enabling/disabling child widgets
        for widget in self.sim_frame.winfo_children():
            if isinstance(widget, (ctk.CTkSlider, ctk.CTkLabel, ctk.CTkFrame)):
                try:
                    widget.configure(state="normal" if mode == "simulation" else "disabled")
                except ValueError:
                    # If widget doesn't support state, try with its children
                    for child in widget.winfo_children():
                        child.configure(state="normal" if mode == "simulation" else "disabled")
        
        # Toggle speed slider based on mode
        speed_state = "normal" if mode != "simulation" else "disabled"
        for widget in self.speed_frame.winfo_children():
            if isinstance(widget, (ctk.CTkSlider, ctk.CTkLabel)):
                widget.configure(state=speed_state)
        
        # Toggle buttons based on mode
        self.game_button.configure(state="normal" if mode != "simulation" else "disabled")
        self.sim_button.configure(state="normal" if mode == "simulation" else "disabled")
    
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
            logging.info("Simulation thread started")
            self.simulation_results = {}
            total_sims = len(self.algorithms) * self.num_simulations.get()
            logging.info(f"Planning to run {total_sims} total simulations")
            
            try:
                progress_window = self.create_progress_window(total_sims)
                logging.info("Progress window created")
                
                for algo_name, algo_id, _ in self.algorithms:
                    logging.info(f"Starting simulations for algorithm: {algo_id}")
                    scores = []
                    
                    for i in range(self.num_simulations.get()):
                        logging.debug(f"Running simulation {i+1} for {algo_id}")
                        try:
                            # Create a new game instance for each simulation in headless mode
                            game = Game(
                                start_with_ai=True,
                                ai_algorithm=algo_id,
                                speed=30,
                                headless=True  # Run without pygame initialization
                            )
                            logging.debug(f"Game instance created for {algo_id}")
                            
                            score = game.run_headless()
                            logging.debug(f"Simulation completed. Score: {score}")
                            scores.append(score)
                            
                            # Update progress
                            progress = ((len(scores) + (self.algorithms.index((algo_name, algo_id, _)) * 
                                       self.num_simulations.get())) / total_sims) * 100
                            
                            # Update progress in the main thread
                            self.root.after(0, progress_window.update_progress, progress)
                            
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
                # Show results in the main thread
                self.root.after(0, lambda: [progress_window.destroy(), self.show_simulation_results()])
            
            except Exception as e:
                logging.error(f"Critical simulation error: {str(e)}")
                logging.error(traceback.format_exc())
                self.root.after(0, lambda: self.show_error_dialog(str(e)))
                if 'progress_window' in locals():
                    self.root.after(0, progress_window.destroy)
            finally:
                # Re-enable buttons
                self.root.after(0, self.enable_buttons)
        
        # Disable buttons during simulation
        self.sim_button.configure(state="disabled")
        self.game_button.configure(state="disabled")
        
        # Run simulation in a separate thread
        sim_thread = threading.Thread(target=run_sim)
        sim_thread.start()
        logging.info("Simulation thread launched")
    
    def enable_buttons(self):
        logging.info("Re-enabling buttons")
        self.sim_button.configure(state="normal")
        self.game_button.configure(state="normal")
    
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
    
    def create_progress_window(self, total_sims):
        progress_window = SimulationProgress(self.root, total_sims)
        return progress_window
    
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