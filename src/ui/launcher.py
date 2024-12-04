import tkinter as tk
from tkinter import ttk
from src.game.game import Game
from src.ai import AI_ALGORITHMS

class GameLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake Game Launcher")
        self.root.geometry("500x800")  # Made taller to ensure space for button
        self.root.resizable(False, False)
        self.root.configure(bg='#2E2E2E')  # Dark background
        
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
        # Main container
        container = tk.Frame(self.root, bg='#2E2E2E')
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_label = tk.Label(
            container, 
            text="🐍 Snake Game",
            font=('Helvetica', 28, 'bold'),
            fg='white',
            bg='#2E2E2E'
        )
        title_label.pack(pady=(0, 30))
        
        # Game Mode Frame
        mode_frame = tk.LabelFrame(container, text="Game Mode", 
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
        
        # AI Algorithm Frame
        self.ai_frame = tk.LabelFrame(container, text="AI Algorithm",
                                    font=('Helvetica', 14),
                                    fg='white', bg='#2E2E2E',
                                    padx=15, pady=15)
        self.ai_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.algorithm = tk.StringVar(value="astar")
        self.radio_buttons = []
        
        algorithms = [
            ("🎯 A* Pathfinding", "astar", "Optimal path finding to food"),
            ("🌊 BFS Pathfinding", "bfs", "Breadth-first search for shortest path"),
            ("🔄 Advanced Hamiltonian", "advanced_hamiltonian", "Optimized safe path"),
            ("🤖 Hybrid A*/Hamiltonian", "hybrid", "Adaptive strategy switching"),
            ("🔍 DFS Exploration", "dfs", "Depth-first exploration"),
            ("🎲 Random Walk", "random", "Random valid moves"),
            ("⚡ Greedy Best-First", "greedy", "Always moves towards food")
        ]
        
        for text, value, desc in algorithms:
            frame = tk.Frame(self.ai_frame, bg='#2E2E2E')
            frame.pack(fill=tk.X, pady=5)
            
            radio = tk.Radiobutton(
                frame,
                text=text,
                variable=self.algorithm,
                value=value,
                font=('Helvetica', 14),
                fg='white', bg='#2E2E2E',
                selectcolor='#2E2E2E'
            )
            radio.pack(side=tk.LEFT)
            self.radio_buttons.append(radio)
            
            tk.Label(
                frame,
                text=desc,
                font=('Helvetica', 12),
                fg='white', bg='#2E2E2E'
            ).pack(side=tk.LEFT, padx=10)
        
        # Game Speed Frame
        speed_frame = tk.LabelFrame(container, text="Game Speed",
                                  font=('Helvetica', 14),
                                  fg='white', bg='#2E2E2E',
                                  padx=15, pady=15)
        speed_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.speed = tk.IntVar(value=10)
        
        speed_label = tk.Label(
            speed_frame,
            text="Speed (FPS):",
            font=('Helvetica', 16),
            fg='white', bg='#2E2E2E'
        )
        speed_label.pack(side=tk.LEFT)
        
        self.fps_label = tk.Label(
            speed_frame,
            text="10",
            font=('Helvetica', 16),
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
        
        # Start Button
        self.start_button = tk.Button(
            container,
            text="▶  Start Game",
            font=('Helvetica', 20, 'bold'),
            bg='#4CAF50',
            fg='black',
            activebackground='#45a049',
            activeforeground='black',
            relief=tk.RAISED,
            command=self.start_game,
            width=20,
            height=2
        )
        self.start_button.pack(pady=40)
        
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