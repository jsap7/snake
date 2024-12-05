import customtkinter as ctk
from src.game.game import Game

class GameLauncher:
    def __init__(self):
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
        
        self.create_widgets()
    
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
        
        # Mode Selection
        mode_buttons_frame = ctk.CTkFrame(mode_frame)
        mode_buttons_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkRadioButton(
            mode_buttons_frame,
            text="👤 Human",
            variable=self.control_mode,
            value="human",
            command=self.toggle_ai_options,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=20)
        
        ctk.CTkRadioButton(
            mode_buttons_frame,
            text="🤖 AI",
            variable=self.control_mode,
            value="ai",
            command=self.toggle_ai_options,
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=20)
        
        # Game Speed Frame
        speed_frame = ctk.CTkFrame(left_column)
        speed_frame.pack(fill="x")
        
        speed_label = ctk.CTkLabel(
            speed_frame,
            text="Game Speed",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        speed_label.pack(pady=(10, 5))
        
        speed_slider_frame = ctk.CTkFrame(speed_frame)
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
        
        # Right Column - AI Algorithms
        right_column = ctk.CTkFrame(columns_frame)
        right_column.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        algorithms_label = ctk.CTkLabel(
            right_column,
            text="AI Algorithm",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        algorithms_label.pack(pady=(10, 5))
        
        # Scrollable frame for algorithms - make it wider
        algorithms_scroll = ctk.CTkScrollableFrame(
            right_column,
            height=350,
            width=500  # Set a fixed width for the scrollable frame
        )
        algorithms_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.radio_buttons = []
        
        algorithms = [
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
        
        for text, value, desc in algorithms:
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
        
        # Start Button
        self.start_button = ctk.CTkButton(
            container,
            text="▶  Start Game",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_game,
            width=200,
            height=40
        )
        self.start_button.pack(pady=20)
        
        # Initial state
        self.toggle_ai_options()
    
    def update_speed_label(self, value):
        self.fps_label.configure(text=f"{int(float(value))} FPS")
    
    def toggle_ai_options(self):
        state = "normal" if self.control_mode.get() == "ai" else "disabled"
        for radio in self.radio_buttons:
            radio.configure(state=state)
    
    def start_game(self):
        self.root.withdraw()
        game = Game(
            start_with_ai=self.control_mode.get() == "ai",
            ai_algorithm=self.algorithm.get(),
            speed=self.speed.get()
        )
        game.run()
        self.root.deiconify()
    
    def run(self):
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.root.mainloop()