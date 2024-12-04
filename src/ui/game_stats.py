import tkinter as tk
from tkinter import ttk
import time

class GameStats:
    def __init__(self, algorithm_name=None, speed_callback=None, pause_callback=None):
        self.window = tk.Toplevel()
        self.window.title("Snake Game Stats")
        self.window.geometry("400x600")
        self.window.resizable(False, False)
        
        # Configure theme and styles
        try:
            self.window.tk.call("source", "azure.tcl")
            self.window.tk.call("set_theme", "dark")
        except tk.TclError:
            try:
                self.window.tk.call("set_theme", "dark")
            except tk.TclError:
                pass
        
        # Statistics variables
        self.score = tk.StringVar(value="0")
        self.turns = tk.StringVar(value="0")
        self.cells_traveled = tk.StringVar(value="0")
        self.efficiency = tk.StringVar(value="0.00%")
        self.time_elapsed = tk.StringVar(value="0:00")
        self.highest_score = 0
        self.start_time = time.time()
        
        # Callbacks
        self.speed_callback = speed_callback
        self.pause_callback = pause_callback
        self.algorithm_name = algorithm_name
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('Title.TLabel', 
                           font=('Helvetica', 24, 'bold'),
                           padding=10)
        self.style.configure('Header.TLabel', 
                           font=('Helvetica', 16, 'bold'),
                           padding=5)
        self.style.configure('Stats.TLabel', 
                           font=('Helvetica', 14),
                           padding=5)
        self.style.configure('Big.TButton', 
                           font=('Helvetica', 14, 'bold'),
                           padding=10)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container with padding
        container = ttk.Frame(self.window, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Title Section
        title_frame = ttk.Frame(container)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            title_frame,
            text="Game Statistics",
            style='Title.TLabel'
        ).pack(anchor=tk.CENTER)
        
        # Algorithm Section (if in AI mode)
        if self.algorithm_name:
            algo_frame = ttk.LabelFrame(container, text="Algorithm", padding=10)
            algo_frame.pack(fill=tk.X, pady=(0, 15))
            
            ttk.Label(
                algo_frame,
                text=self.algorithm_name,
                style='Stats.TLabel'
            ).pack(anchor=tk.W)
        
        # Stats Section
        stats_frame = ttk.LabelFrame(container, text="Performance", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Grid for stats
        stats = [
            ("Score:", self.score),
            ("High Score:", str(self.highest_score)),
            ("Turns Made:", self.turns),
            ("Cells Traveled:", self.cells_traveled),
            ("Efficiency:", self.efficiency),
            ("Time:", self.time_elapsed)
        ]
        
        for i, (label, var) in enumerate(stats):
            frame = ttk.Frame(stats_frame)
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(
                frame,
                text=label,
                style='Header.TLabel'
            ).pack(side=tk.LEFT)
            
            ttk.Label(
                frame,
                textvariable=var if isinstance(var, tk.StringVar) else None,
                text=var if isinstance(var, str) else None,
                style='Stats.TLabel'
            ).pack(side=tk.RIGHT)
        
        # Controls Section (if in AI mode)
        if self.algorithm_name:
            controls_frame = ttk.LabelFrame(container, text="Controls", padding=10)
            controls_frame.pack(fill=tk.X, pady=(0, 15))
            
            # Speed Control
            speed_frame = ttk.Frame(controls_frame)
            speed_frame.pack(fill=tk.X, pady=(0, 10))
            
            ttk.Label(
                speed_frame,
                text="Speed:",
                style='Header.TLabel'
            ).pack(side=tk.LEFT)
            
            self.speed_var = tk.IntVar(value=10)
            self.speed_label = ttk.Label(
                speed_frame,
                text="10 FPS",
                style='Stats.TLabel'
            )
            self.speed_label.pack(side=tk.RIGHT)
            
            speed_scale = ttk.Scale(
                controls_frame,
                from_=5,
                to=30,
                variable=self.speed_var,
                orient=tk.HORIZONTAL,
                command=self.on_speed_change
            )
            speed_scale.pack(fill=tk.X, pady=(0, 10))
            
            # Pause Button
            self.pause_var = tk.BooleanVar(value=False)
            self.pause_button = ttk.Button(
                controls_frame,
                text="⏸ Pause",
                style='Big.TButton',
                command=self.toggle_pause
            )
            self.pause_button.pack(fill=tk.X)
        
        # Position window to the right of game window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) + 400
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make sure window stays on top
        self.window.attributes('-topmost', True)
    
    def on_speed_change(self, value):
        fps = int(float(value))
        self.speed_label.configure(text=f"{fps} FPS")
        if self.speed_callback:
            self.speed_callback(fps)
    
    def toggle_pause(self):
        self.pause_var.set(not self.pause_var.get())
        self.pause_button.configure(
            text="▶ Resume" if self.pause_var.get() else "⏸ Pause"
        )
        if self.pause_callback:
            self.pause_callback(self.pause_var.get())
    
    def update_stats(self, score, turns, length, grid_size):
        # Update basic stats
        self.score.set(str(score))
        
        # Update turns (direction changes)
        self.turns.set(str(turns))
        
        # Update cells traveled
        cells_traveled = int(self.cells_traveled.get().split()[0]) + 1
        self.cells_traveled.set(f"{cells_traveled}")
        
        # Calculate efficiency (score / cells traveled)
        if cells_traveled > 0:
            efficiency = (score / cells_traveled) * 100
            self.efficiency.set(f"{efficiency:.2f}%")
        
        # Update time
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.time_elapsed.set(f"{minutes}:{seconds:02d}")
        
        # Update highest score
        if score > self.highest_score:
            self.highest_score = score
        
        # Process pending events to ensure UI updates
        self.window.update()
    
    def reset(self):
        self.start_time = time.time()
        self.cells_traveled.set("0")
        self.efficiency.set("0.00%")
        self.time_elapsed.set("0:00")
        
        # Reset pause state if needed
        if hasattr(self, 'pause_var'):
            self.pause_var.set(False)
            self.pause_button.configure(text="⏸ Pause")
    
    def destroy(self):
        self.window.destroy()