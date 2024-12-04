import tkinter as tk
from tkinter import ttk
from src.game.game import Game
from src.ai import AI_ALGORITHMS

class GameLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake Game Launcher")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Configure theme and styles
        try:
            self.root.tk.call("source", "src/ui/themes/azure.tcl")
            self.root.tk.call("set_theme", "dark")
        except tk.TclError:
            try:
                self.root.tk.call("set_theme", "dark")
            except tk.TclError:
                pass
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', 
                           font=('Helvetica', 28, 'bold'),
                           padding=15)
        self.style.configure('Header.TLabel',
                           font=('Helvetica', 16),
                           padding=10)
        self.style.configure('Description.TLabel',
                           font=('Helvetica', 12),
                           padding=5)
        self.style.configure('TRadiobutton',
                           font=('Helvetica', 14))
        self.style.layout('TRadiobutton', [
            ('Radiobutton.padding', {
                'children': [
                    ('Radiobutton.indicator', {'side': 'left', 'sticky': ''}),
                    ('Radiobutton.focus', {
                        'children': [
                            ('Radiobutton.label', {'sticky': 'nswe'})
                        ],
                        'side': 'left',
                        'sticky': ''
                    })
                ],
                'sticky': 'nswe'
            })
        ])
        
        # Configure the indicator colors
        self.style.map('TRadiobutton',
                      indicatorcolor=[('selected', '#4CAF50'),  # Green when selected
                                    ('!selected', '#FFFFFF')],  # White when not selected
                      indicatorrelief=[('pressed', 'sunken'),
                                     ('!pressed', 'raised')])
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title_label = ttk.Label(
            container, 
            text="🐍 Snake Game",
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 30))
        
        # Game Mode Frame
        mode_frame = ttk.LabelFrame(container, text="Game Mode", padding=15)
        mode_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.control_mode = tk.StringVar(value="human")
        
        # Mode Selection
        ttk.Radiobutton(
            mode_frame, 
            text="👤 Human",
            variable=self.control_mode,
            value="human",
            command=self.toggle_ai_options,
            style='TRadiobutton'
        ).pack(side=tk.LEFT, padx=20)
        
        ttk.Radiobutton(
            mode_frame, 
            text="🤖 AI",
            variable=self.control_mode,
            value="ai",
            command=self.toggle_ai_options,
            style='TRadiobutton'
        ).pack(side=tk.LEFT, padx=20)
        
        # AI Algorithm Frame
        self.ai_frame = ttk.LabelFrame(container, text="AI Algorithm", padding=15)
        self.ai_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.algorithm = tk.StringVar(value="astar")
        self.radio_buttons = []
        
        algorithms = [
            ("🎯 A* Pathfinding", "astar", "Optimal path finding to food"),
            ("🌊 BFS Pathfinding", "bfs", "Breadth-first search for shortest path"),
            ("🔄 Hamiltonian + Shortcuts", "hamiltonian", "Safe path with optimizations"),
            ("🔍 DFS Exploration", "dfs", "Depth-first exploration"),
            ("🎲 Random Walk", "random", "Random valid moves")
        ]
        
        for text, value, desc in algorithms:
            frame = ttk.Frame(self.ai_frame)
            frame.pack(fill=tk.X, pady=5)
            
            radio = ttk.Radiobutton(
                frame,
                text=text,
                variable=self.algorithm,
                value=value,
                style='TRadiobutton'
            )
            radio.pack(side=tk.LEFT)
            self.radio_buttons.append(radio)
            
            ttk.Label(
                frame,
                text=desc,
                style='Description.TLabel'
            ).pack(side=tk.LEFT, padx=10)
        
        # Game Speed Frame
        speed_frame = ttk.LabelFrame(container, text="Game Speed", padding=15)
        speed_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.speed = tk.IntVar(value=10)
        
        speed_label = ttk.Label(
            speed_frame,
            text="Speed (FPS):",
            style='Header.TLabel'
        )
        speed_label.pack(side=tk.LEFT)
        
        self.fps_label = ttk.Label(
            speed_frame,
            text="10",
            style='Header.TLabel'
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
        self.start_button = ttk.Button(
            container,
            text="▶  Start Game",
            style='Accent.TButton',
            command=self.start_game
        )
        self.start_button.pack(pady=30)
        
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