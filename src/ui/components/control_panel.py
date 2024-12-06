import customtkinter as ctk

class ControlPanel:
    def __init__(self, parent, callbacks):
        self.parent = parent
        self.callbacks = callbacks
        
        # Variables
        self.control_mode = ctk.StringVar(value="human")
        self.algorithm = ctk.StringVar(value="astar")
        self.speed = ctk.IntVar(value=10)
        self.num_simulations = ctk.IntVar(value=10)
        self.population_size = ctk.IntVar(value=50)
        self.generation_limit = ctk.IntVar(value=20)
        
        self._create_widgets()
    
    def _create_widgets(self):
        # Create main container
        self.container = ctk.CTkFrame(self.parent)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            self.container,
            text=" Snake Game",
            font=ctk.CTkFont(size=32, weight="bold"),
        )
        title_label.pack(pady=(0, 20))
        
        # Create columns frame
        columns_frame = ctk.CTkFrame(self.container)
        columns_frame.pack(fill="both", expand=True, padx=10)
        
        # Create left column (controls)
        self._create_left_column(columns_frame)
        
        # Create right column (algorithms)
        self._create_right_column(columns_frame)
        
        # Create buttons frame
        self._create_buttons_frame()
    
    def _create_left_column(self, parent):
        left_column = ctk.CTkFrame(parent)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Game Mode Frame
        self._create_mode_frame(left_column)
        
        # Game Speed Frame
        self._create_speed_frame(left_column)
        
        # Simulation Settings Frame
        self._create_simulation_frame(left_column)
        
        # Training Settings Frame
        self._create_training_frame(left_column)
    
    def _create_right_column(self, parent):
        # Implementation of right column with algorithm selection
        pass
    
    def _create_mode_frame(self, parent):
        # Implementation of mode selection frame
        pass
    
    def _create_speed_frame(self, parent):
        # Implementation of speed control frame
        pass
    
    def _create_simulation_frame(self, parent):
        # Implementation of simulation settings frame
        pass
    
    def _create_training_frame(self, parent):
        # Implementation of training settings frame
        pass
    
    def _create_buttons_frame(self):
        # Implementation of buttons frame
        pass
    
    def get_settings(self):
        """Return current control settings"""
        return {
            'mode': self.control_mode.get(),
            'algorithm': self.algorithm.get(),
            'speed': self.speed.get(),
            'num_simulations': self.num_simulations.get(),
            'population_size': self.population_size.get(),
            'generation_limit': self.generation_limit.get()
        } 