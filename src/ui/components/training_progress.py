import customtkinter as ctk

class TrainingProgress(ctk.CTkToplevel):
    def __init__(self, parent, total):
        super().__init__(parent)
        self.title("Training Progress")
        self.geometry("400x150")
        
        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.total = total
        self._create_widgets()
    
    def _create_widgets(self):
        # Progress label
        self.label = ctk.CTkLabel(
            self,
            text=f"Training Generation 0/{self.total}...",
            font=ctk.CTkFont(size=14)
        )
        self.label.pack(pady=20)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=20, padx=20, fill="x")
        self.progress_bar.set(0)
    
    def update_progress(self, progress):
        """Update progress bar and label"""
        self.progress_bar.set(progress / 100)
        generation = int((progress / 100) * self.total)
        self.label.configure(text=f"Training Generation {generation}/{self.total}...")
        self.update() 