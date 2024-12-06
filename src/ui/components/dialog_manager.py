import customtkinter as ctk
import logging

class DialogManager:
    def __init__(self, parent):
        self.parent = parent
    
    def show_message(self, title, message):
        """Show a message dialog"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(title)
        dialog.geometry("400x200")
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        label = ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=350
        )
        label.pack(pady=20, padx=20)
        
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        )
        ok_button.pack(pady=20)
    
    def show_error(self, error_message):
        """Show an error dialog"""
        logging.info("Showing error dialog")
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Error")
        dialog.geometry("400x200")
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        error_label = ctk.CTkLabel(
            dialog,
            text=f"An error occurred:\n\n{error_message}",
            wraplength=350
        )
        error_label.pack(pady=20, padx=20)
        
        ok_button = ctk.CTkButton(
            dialog,
            text="OK",
            command=dialog.destroy
        )
        ok_button.pack(pady=20) 