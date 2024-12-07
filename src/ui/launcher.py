import customtkinter as ctk
import logging
import traceback
import queue
import threading
from src.game.game import Game
from src.ui.components.progress_window import SimulationProgress
from src.ui.components.simulation_manager import SimulationManager
from src.ui.components.results_window import SimulationResults
from src.ui.components.training_manager import TrainingManager
from src.ui.components.dialog_manager import DialogManager
from src.ui.components.algorithm_manager import AlgorithmManager
from src.ui.components.training_view import TrainingView
from src.ui.components.training_progress import TrainingProgress
from src.utils.settings import SNAKE_COLOR_SCHEMES

# Configure logging
logging.getLogger('matplotlib.font_manager').disabled = True
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simulation.log'),
    ]
)
logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)

class GameLauncher:
    # Initialization methods
    def __init__(self):
        logging.info("Initializing GameLauncher")
        self._setup_window()
        self._init_variables()
        self._init_managers()
        self.create_widgets()
        logging.info("GameLauncher initialized successfully")
    
    def _setup_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("Snake Game Launcher")
        self.root.geometry("1300x900")
        self.root.resizable(False, False)
    
    def _init_variables(self):
        self.result_queue = queue.Queue()
        self.control_mode = ctk.StringVar(value="human")
        self.algorithm = ctk.StringVar(value="astar")
        self.speed = ctk.IntVar(value=10)
        self.num_simulations = ctk.IntVar(value=10)
        self.simulation_results = {}
        
        # Clear simulation log file
        with open("simulation.log", "w") as f:
            f.write("")
    
    def _init_managers(self):
        self.dialog_manager = DialogManager(self.root)
        self.algorithm_manager = None  # Will be initialized in create_widgets
        self.training_view = None      # Will be initialized in create_widgets
    
    # UI Creation and Update Methods
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
        
        # Game Settings Frame (add this after speed frame)
        self.settings_frame = ctk.CTkFrame(left_column)
        self.settings_frame.pack(fill="x", pady=(0, 20))
        
        settings_label = ctk.CTkLabel(
            self.settings_frame,
            text="Game Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        settings_label.pack(pady=(10, 5))
        
        # Color Selection Frame
        color_frame = ctk.CTkFrame(self.settings_frame)
        color_frame.pack(fill="x", padx=20, pady=10)
        
        color_label = ctk.CTkLabel(
            color_frame,
            text="Snake Color:",
            font=ctk.CTkFont(size=14)
        )
        color_label.pack(side="left", padx=10)
        
        # Initialize color variable
        self.color_var = ctk.StringVar(value="blue")
        
        # Create color dropdown
        color_menu = ctk.CTkOptionMenu(
            color_frame,
            values=list(SNAKE_COLOR_SCHEMES.keys()),
            variable=self.color_var,
            width=120
        )
        color_menu.pack(side="left", padx=10)
        
        # Color Preview Frame
        preview_frame = ctk.CTkFrame(color_frame, width=30, height=30)
        preview_frame.pack(side="right", padx=10)
        
        # Function to update preview color
        def update_preview(*args):
            scheme = SNAKE_COLOR_SCHEMES[self.color_var.get()]
            preview_frame.configure(fg_color=self.rgb_to_hex(scheme['head']))
        
        # Bind color change to preview update
        self.color_var.trace_add("write", update_preview)
        
        # Initial preview update
        update_preview()
        
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
        
        # Initialize algorithm manager first
        self.algorithm_manager = AlgorithmManager(right_column, self.algorithm)
        
        # Now initialize training view and add its frame to left column
        self.training_view = TrainingView(self.root, self.dialog_manager, self.algorithm_manager)
        self.training_frame = self.training_view.training_frame
        self.training_frame.pack(in_=left_column, fill="x", pady=(0, 20))
        
        # Buttons Frame
        self.buttons_frame = ctk.CTkFrame(container)
        self.buttons_frame.pack(pady=20)
        
        # Play Game Button (for human/AI mode)
        self.game_button = ctk.CTkButton(
            self.buttons_frame,
            text="▶  Play Game",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_game,
            width=200,
            height=40
        )
        
        # Run Simulation Button
        self.simulation_button = ctk.CTkButton(
            self.buttons_frame,
            text="📊 Run Simulation",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_simulation,
            width=200,
            height=40,
            fg_color="#2B7821",  # Green color
            hover_color="#1F5817"
        )
        
        # Training Button
        self.train_button = ctk.CTkButton(
            self.buttons_frame,
            text="🧬 Start Training",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_training,
            width=200,
            height=40,
            fg_color="#2B7821",  # Green color
            hover_color="#1F5817"
        )
        
        # Store train button reference in training view
        self.training_view.train_button = self.train_button
        
        # Initial state
        self.toggle_options()
    
    def update_speed_label(self, value):
        self.fps_label.configure(text=f"{int(float(value))} FPS")
    
    def update_sim_label(self, value):
        self.sim_count_label.configure(text=f"{int(float(value))} games per AI")
    
    def toggle_options(self):
        """Update UI based on selected mode"""
        mode = self.control_mode.get()
        
        # Clear buttons frame
        for widget in self.buttons_frame.winfo_children():
            widget.pack_forget()
        
        # Update algorithm buttons state
        ai_state = "normal" if mode == "ai" else "disabled"
        self.algorithm_manager.set_buttons_state(ai_state)
        
        # Toggle simulation settings
        sim_state = "normal" if mode == "simulation" else "disabled"
        for widget in self.sim_frame.winfo_children():
            if isinstance(widget, (ctk.CTkSlider, ctk.CTkLabel)):  # Remove CTkFrame
                try:
                    widget.configure(state=sim_state)
                except (ValueError, AttributeError):
                    continue
            elif isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, (ctk.CTkSlider, ctk.CTkLabel)):
                        try:
                            child.configure(state=sim_state)
                        except (ValueError, AttributeError):
                            continue
        
        # Toggle training settings
        train_state = "normal" if mode == "training" else "disabled"
        for widget in self.training_frame.winfo_children():
            if isinstance(widget, (ctk.CTkSlider, ctk.CTkLabel)):  # Remove CTkFrame
                try:
                    widget.configure(state=train_state)
                except (ValueError, AttributeError):
                    continue
            elif isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, (ctk.CTkSlider, ctk.CTkLabel)):
                        try:
                            child.configure(state=train_state)
                        except (ValueError, AttributeError):
                            continue
        
        # Show appropriate buttons based on mode
        if mode in ["human", "ai"]:
            self.game_button.pack(side="left", padx=10)
        elif mode == "simulation":
            self.simulation_button.pack(side="left", padx=10)
        elif mode == "training":
            self.train_button.pack(side="left", padx=10)
    
    # Game Control Methods
    def start_game(self):
        self.root.withdraw()  # Hide launcher window
        try:
            game = Game(
                start_with_ai=self.control_mode.get() == "ai",
                ai_algorithm=self.algorithm.get(),
                speed=self.speed.get(),
                color_scheme=self.color_var.get()
            )
            game.run()
        finally:
            # Always show launcher window again, regardless of how game ends
            self.root.deiconify()
    
    def start_simulation(self):
        logging.info("Starting simulation process")
        sim_manager = SimulationManager(
            self.root,
            self.algorithm_manager.algorithms,
            self.num_simulations.get()
        )
        
        def run_sim():
            try:
                self.root.after(0, lambda: self.create_and_store_progress_window(
                    len(self.algorithm_manager.algorithms) * self.num_simulations.get()
                ))
                
                result_type, result_data = sim_manager.run_simulation(
                    lambda p: self.root.after(0, lambda: self.update_progress(p))
                )
                
                self.result_queue.put((result_type, result_data))
                
            except Exception as e:
                logging.error(f"Critical simulation error: {str(e)}")
                logging.error(traceback.format_exc())
                self.result_queue.put(("error", str(e)))
        
        self.train_button.configure(state="disabled")
        self.game_button.configure(state="disabled")
        
        sim_thread = threading.Thread(target=run_sim)
        sim_thread.daemon = True
        sim_thread.start()
        
        self.root.after(100, self.check_simulation_results)
    
    def start_training(self):
        """Start genetic algorithm training"""
        trainer = TrainingManager(
            population_size=self.training_view.population_size.get(),
            generation_limit=self.training_view.generation_limit.get()
        )
        
        progress_window = self.create_progress_window(self.training_view.generation_limit.get())
        self.training_view.start_training(trainer, progress_window)
    
    # Progress Tracking Methods
    def create_progress_window(self, total_generations):
        """Create a progress window for training"""
        return TrainingProgress(self.root, total_generations)
    
    def create_and_store_progress_window(self, total_sims):
        self.progress_window = SimulationProgress(self.root, total_sims)
    
    def update_progress(self, progress):
        if hasattr(self, 'progress_window'):
            self.progress_window.update_progress(progress)
    
    # Results Handling Methods
    def check_simulation_results(self):
        try:
            result_type, result_data = self.result_queue.get_nowait()
            
            if hasattr(self, 'progress_window'):
                self.progress_window.destroy()
            
            if result_type == "success":
                self.simulation_results = result_data
                self.show_simulation_results()
            else:
                self.dialog_manager.show_error(result_data)
            
            self.enable_buttons()
            
        except queue.Empty:
            self.root.after(100, self.check_simulation_results)
    
    def show_simulation_results(self):
        SimulationResults(self.root, self.simulation_results)
    
    def enable_buttons(self):
        """Re-enable buttons after training/simulation"""
        self.game_button.configure(state="normal")
        self.train_button.configure(state="normal")
    
    # Main Run Method
    def run(self):
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()
    
    def rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color string"""
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
