import tkinter as tk
from tkinter import ttk
from src.game.game import Game
from src.ai import AI_ALGORITHMS

class GameLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake Game Launcher")
        self.root.geometry("800x600")  # Wider but shorter window
        self.root.resizable(False, False)
        self.root.configure(bg='#2E2E2E')
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', 
                           font=('Helvetica', 28, 'bold'),
                           padding=15,
                           background='#2E2E2E',
                           foreground='white')
        self.style.configure('Header.TLabel',
                           font=('Helvetica', 16),
                           padding=10,
                           background='#2E2E2E',
                           foreground='white')
        self.style.configure('Description.TLabel',
                           font=('Helvetica', 12),
                           padding=5,
                           background='#2E2E2E',
                           foreground='white')
        self.style.configure('TRadiobutton',
                           font=('Helvetica', 14),
                           background='#2E2E2E',
                           foreground='white')
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main container with padding
        container = tk.Frame(self.root, bg='#2E2E2E')
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with snake emoji
        title_frame = tk.Frame(container, bg='#2E2E2E')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame, 
            text="🐍 Snake Game",
            font=('Helvetica', 32, 'bold'),
            fg='white',
            bg='#2E2E2E'
        )
        title_label.pack()
        
        # Create two columns
        columns_frame = tk.Frame(container, bg='#2E2E2E')
        columns_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column for game mode and speed
        left_column = tk.Frame(columns_frame, bg='#2E2E2E')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Game Mode Frame
        mode_frame = tk.LabelFrame(left_column, text="Game Mode", 
                                 font=('Helvetica', 14),
                                 fg='white', bg='#2E2E2E',
                                 padx=15, pady=15)
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.control_mode = tk.StringVar(value="human")
        
        # Mode Selection
        tk.Radiobutton(
            mode_frame, 
            text="👤 Human",
            variable=self.control_mode,
            value="human",
            command=self.toggle_ai_options,
            font=('Helvetica', 14),
            fg='white', bg='#2E2E2E',
            selectcolor='#2E2E2E'
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Radiobutton(
            mode_frame, 
            text="🤖 AI",
            variable=self.control_mode,
            value="ai",
            command=self.toggle_ai_options,
            font=('Helvetica', 14),
            fg='white', bg='#2E2E2E',
            selectcolor='#2E2E2E'
        ).pack(side=tk.LEFT, padx=20)
        
        # Game Speed Frame
        speed_frame = tk.LabelFrame(left_column, text="Game Speed",
                                  font=('Helvetica', 14),
                                  fg='white', bg='#2E2E2E',
                                  padx=15, pady=15)
        speed_frame.pack(fill=tk.X)
        
        self.speed = tk.IntVar(value=10)
        
        speed_label = tk.Label(
            speed_frame,
            text="Speed (FPS):",
            font=('Helvetica', 14),
            fg='white', bg='#2E2E2E'
        )
        speed_label.pack(side=tk.LEFT)
        
        self.fps_label = tk.Label(
            speed_frame,
            text="10",
            font=('Helvetica', 14),
            fg='white', bg='#2E2E2E'
        )
        self.fps_label.pack(side=tk.RIGHT)
        
        speed_scale = ttk.Scale(
            speed_frame,
            from_=5,
            to=30,
            variable=self.speed,
            orient=tk.HORIZONTAL,
            command=self.update_speed_label
        )
        speed_scale.pack(fill=tk.X, pady=(10, 0))
        
        # Right column for AI algorithms
        right_column = tk.Frame(columns_frame, bg='#2E2E2E')
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # AI Algorithm Frame
        self.ai_frame = tk.LabelFrame(right_column, text="AI Algorithm",
                                    font=('Helvetica', 14),
                                    fg='white', bg='#2E2E2E',
                                    padx=15, pady=15)
        self.ai_frame.pack(fill=tk.BOTH, expand=True)
        
        self.algorithm = tk.StringVar(value="astar")
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
        
        # Create a canvas with scrollbar for algorithms
        canvas = tk.Canvas(self.ai_frame, bg='#2E2E2E', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.ai_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2E2E2E')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack algorithms into scrollable frame
        for text, value, desc in algorithms:
            frame = tk.Frame(scrollable_frame, bg='#2E2E2E')
            frame.pack(fill=tk.X, pady=3)
            
            radio = tk.Radiobutton(
                frame,
                text=text,
                variable=self.algorithm,
                value=value,
                font=('Helvetica', 12),
                fg='white', bg='#2E2E2E',
                selectcolor='#2E2E2E'
            )
            radio.pack(side=tk.LEFT)
            self.radio_buttons.append(radio)
            
            tk.Label(
                frame,
                text=desc,
                font=('Helvetica', 10),
                fg='white', bg='#2E2E2E'
            ).pack(side=tk.LEFT, padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Start Button at the bottom
        self.start_button = tk.Button(
            container,
            text="▶  Start Game",
            font=('Helvetica', 16, 'bold'),
            bg='black',
            fg='white',
            activebackground='black',
            activeforeground='white',
            relief=tk.RAISED,
            command=self.start_game,
            width=20,
            height=1
        )
        self.start_button.pack(pady=20)
        
        # Initial state
        self.toggle_ai_options()
    
    def update_speed_label(self, value):
        self.fps_label.configure(text=str(int(float(value))))
    
    def toggle_ai_options(self):
        state = 'normal' if self.control_mode.get() == "ai" else 'disabled'
        for radio in self.radio_buttons:
            radio.configure(state=state)
    
    def start_game(self):
        self.root.withdraw()
        game = Game(
            start_with_ai=self.control_mode.get() == "ai",
            ai_algorithm=self.algorithm.get()
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