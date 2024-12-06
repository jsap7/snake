import customtkinter as ctk
import logging

class SimulationProgress(ctk.CTkToplevel):
    def __init__(self, parent, total_sims):
        super().__init__(parent)
        self.title("Simulation Progress")
        self.geometry("300x150")
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (parent.winfo_screenwidth() // 2) - (width // 2)
        y = (parent.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.total_sims = total_sims
        self._create_widgets()
    
    def _create_widgets(self):
        self.label = ctk.CTkLabel(
            self,
            text="Running simulations...",
            font=ctk.CTkFont(size=14)
        )
        self.label.pack(pady=20)
        
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=20, padx=20, fill="x")
        self.progress_bar.set(0)
        
        self.percentage_label = ctk.CTkLabel(
            self,
            text="0%",
            font=ctk.CTkFont(size=12)
        )
        self.percentage_label.pack(pady=5)
    
    def update_progress(self, progress):
        try:
            self.progress_bar.set(progress / 100)
            self.percentage_label.configure(text=f"{progress:.1f}%")
            self.update()
        except Exception as e:
            logging.error(f"Error updating progress: {str(e)}") 