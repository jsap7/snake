import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
import json
import os
from datetime import datetime
import threading
import numpy as np
import traceback

class TrainingView:
    def __init__(self, parent, dialog_manager, algorithm_manager):
        self.parent = parent
        self.dialog_manager = dialog_manager
        self.algorithm_manager = algorithm_manager
        
        # Training variables
        self.population_size = ctk.IntVar(value=50)
        self.generation_limit = ctk.IntVar(value=20)
        
        # Create training frame
        self.training_frame = self._create_training_frame()
        self.train_button = None
    
    def _create_training_frame(self):
        frame = ctk.CTkFrame(self.parent)
        
        # Title
        training_label = ctk.CTkLabel(
            frame,
            text="Training Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        training_label.pack(pady=(10, 5))
        
        # Settings Container
        settings_container = ctk.CTkFrame(frame)
        settings_container.pack(fill="x", padx=20, pady=5)
        
        # Population Size
        pop_frame = self._create_setting_frame(
            settings_container,
            "Population Size",
            self.population_size,
            10, 100,
            self._update_pop_label
        )
        pop_frame.pack(fill="x", pady=5)
        
        # Generation Limit
        gen_frame = self._create_setting_frame(
            settings_container,
            "Generation Limit",
            self.generation_limit,
            5, 50,
            self._update_gen_label
        )
        gen_frame.pack(fill="x", pady=5)
        
        return frame
    
    def _create_setting_frame(self, parent, label_text, variable, from_, to, callback):
        frame = ctk.CTkFrame(parent)
        
        label = ctk.CTkLabel(
            frame,
            text=f"{label_text}: {variable.get()}",
            font=ctk.CTkFont(size=14)
        )
        label.pack(side="top", padx=10, pady=(5, 0))
        
        slider = ctk.CTkSlider(
            frame,
            from_=from_,
            to=to,
            variable=variable,
            command=lambda v: callback(label, v)
        )
        slider.pack(fill="x", padx=10, pady=(5, 10))
        
        return frame
    
    def _update_pop_label(self, label, value):
        label.configure(text=f"Population Size: {int(float(value))}")
    
    def _update_gen_label(self, label, value):
        label.configure(text=f"Generation Limit: {int(float(value))}")
    
    def show_training_results(self, genetic_population):
        results_window = ctk.CTkToplevel(self.parent)
        results_window.title("Training Results")
        results_window.geometry("1000x800")
        
        container = ctk.CTkFrame(results_window)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            container,
            text=" Genetic Algorithm Training Results",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 30))
        
        self._create_training_plots(container, genetic_population)
    
    def _create_training_plots(self, container, genetic_population):
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(14, 10))
        fig.patch.set_facecolor('#1E1E1E')
        
        self._plot_fitness_over_generations(plt.subplot2grid((2, 1), (0, 0)), genetic_population)
        self._plot_best_weights(plt.subplot2grid((2, 1), (1, 0)), genetic_population.best_individual)
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=(0, 20))
    
    def _plot_fitness_over_generations(self, ax, genetic_population):
        generations = [stat['generation'] for stat in genetic_population.generation_stats]
        best_fitness = [stat['best_fitness'] for stat in genetic_population.generation_stats]
        avg_fitness = [stat['avg_fitness'] for stat in genetic_population.generation_stats]
        
        ax.plot(generations, best_fitness, label='Best Fitness', color='#2ecc71')
        ax.plot(generations, avg_fitness, label='Average Fitness', color='#3498db')
        ax.set_title('Fitness Over Generations', color='white', pad=20)
        ax.set_xlabel('Generation', color='white')
        ax.set_ylabel('Fitness', color='white')
        ax.legend()
        ax.grid(True, alpha=0.2)
    
    def _plot_best_weights(self, ax, best_individual):
        if best_individual:
            weights = list(best_individual.weights.values())
            labels = list(best_individual.weights.keys())
            x = np.arange(len(labels))
            
            bars = ax.bar(x, weights, color='#e74c3c', alpha=0.8)
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}',
                       ha='center', va='bottom', color='white')
            
            ax.set_title('Best Individual Weights', color='white', pad=20)
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha='right')
            ax.grid(True, alpha=0.2)
            
            # Add explanation text
            explanation = (
                "Weight Importance:\n"
                "• Higher values = stronger influence\n"
                "• Negative values = avoidance behavior\n"
                "• Positive values = seeking behavior"
            )
            props = dict(boxstyle='round', facecolor='#2C3E50', alpha=0.8)
            ax.text(1.02, 0.02, explanation,
                   transform=ax.transAxes,
                   fontsize=10,
                   verticalalignment='bottom',
                   bbox=props)
    
    def start_training(self, trainer, progress_window):
        def train():
            try:
                result_type, result_data = trainer.start_training(
                    lambda p: self.parent.after(0, lambda: progress_window.update_progress(p))
                )
                
                if result_type == "success":
                    model_info = trainer.save_model()
                    if model_info:
                        model_name, model_path = model_info
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        
                        # Add new model to algorithms
                        self.algorithm_manager.add_trained_model(
                            timestamp,
                            trainer.genetic_population.best_fitness
                        )
                        
                        # Show success message and training results
                        self.parent.after(0, lambda: [
                            self.dialog_manager.show_message(
                                "Success", 
                                f"Model saved as {model_name} and added to algorithms list"
                            ),
                            self.show_training_results(trainer.genetic_population)
                        ])
                else:
                    self.parent.after(0, lambda: self.dialog_manager.show_error(result_data))
                
            except Exception as e:
                logging.error(f"Training error: {str(e)}")
                logging.error(traceback.format_exc())
                self.parent.after(0, lambda: self.dialog_manager.show_error(str(e)))
            finally:
                self.parent.after(0, progress_window.destroy)
                if self.train_button:
                    self.parent.after(0, lambda: self.train_button.configure(state="normal"))
        
        if self.train_button:
            self.train_button.configure(state="disabled")
        
        train_thread = threading.Thread(target=train)
        train_thread.daemon = True
        train_thread.start() 