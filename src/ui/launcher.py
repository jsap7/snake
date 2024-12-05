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
        self.root.geometry("1000x650")
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
        
        # Scrollable frame for algorithms
        algorithms_scroll = ctk.CTkScrollableFrame(
            right_column,
            height=350,
            width=500  # Set fixed width for better layout
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
            self.radio_buttons.append(radio)
            
            desc_label = ctk.CTkLabel(
                frame,
                text=desc,
                font=ctk.CTkFont(size=12),
                wraplength=250,  # Adjusted wraplength
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
        results_window.geometry("1000x800")  # Larger window for better visibility
        
        # Create main container
        container = ctk.CTkFrame(results_window)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            container,
            text="🎮 AI Performance Analysis",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Stats Frame
        stats_frame = ctk.CTkFrame(container)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        # Create matplotlib figure with dark style
        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        fig.patch.set_facecolor('#2b2b2b')
        
        algorithms = list(self.simulation_results.keys())
        avg_scores = [self.simulation_results[algo]['avg'] for algo in algorithms]
        max_scores = [self.simulation_results[algo]['max'] for algo in algorithms]
        
        # Plot average and max scores
        x = np.arange(len(algorithms))
        width = 0.35
        
        ax1.bar(x - width/2, avg_scores, width, label='Average Score', color='#1f77b4')
        ax1.bar(x + width/2, max_scores, width, label='Max Score', color='#2ca02c')
        ax1.set_title('Performance Comparison', color='white', pad=20)
        ax1.set_xticks(x)
        ax1.set_xticklabels(algorithms, rotation=45, ha='right', color='white')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Box plot
        ax2.boxplot([self.simulation_results[algo]['scores'] for algo in algorithms])
        ax2.set_title('Score Distribution', color='white', pad=20)
        ax2.set_xticklabels(algorithms, rotation=45, ha='right', color='white')
        ax2.grid(True, alpha=0.3)
        
        # Adjust layout
        plt.tight_layout()
        
        # Embed plot
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Add detailed stats table
        stats_table = ctk.CTkFrame(container)
        stats_table.pack(fill="x", pady=(20, 0))
        
        # Headers
        headers = ["Algorithm", "Games", "Avg Score", "Max Score", "Min Score", "Std Dev"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                stats_table,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold")
            ).grid(row=0, column=i, padx=10, pady=5, sticky="w")
        
        # Data rows
        for i, algo in enumerate(algorithms, 1):
            data = self.simulation_results[algo]
            row_data = [
                algo,
                str(len(data['scores'])),
                f"{data['avg']:.2f}",
                str(data['max']),
                str(min(data['scores'])),
                f"{np.std(data['scores']):.2f}"
            ]
            for j, value in enumerate(row_data):
                ctk.CTkLabel(
                    stats_table,
                    text=value,
                    font=ctk.CTkFont(size=12)
                ).grid(row=i, column=j, padx=10, pady=5, sticky="w")
        
        # Save results button
        save_button = ctk.CTkButton(
            container,
            text="💾 Save Results",
            font=ctk.CTkFont(size=14),
            command=lambda: self.save_simulation_results(),
            width=150
        )
        save_button.pack(pady=20)
    
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