import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from datetime import datetime
import json
import os
import logging

class SimulationResults(ctk.CTkToplevel):
    def __init__(self, parent, results):
        super().__init__(parent)
        self.title("Simulation Results")
        self.geometry("1400x900")
        self.results = results
        self._create_widgets()
    
    def _create_widgets(self):
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            container,
            text="🎮 AI Performance Analysis",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(0, 30))
        
        self._create_plots(container)
        self._create_save_button(container)
    
    def _create_plots(self, container):
        plt.style.use('dark_background')
        fig = plt.figure(figsize=(14, 10))
        fig.patch.set_facecolor('#1E1E1E')
        
        self._plot_performance_comparison(plt.subplot2grid((2, 1), (0, 0)))
        self._plot_algorithm_rankings(plt.subplot2grid((2, 1), (1, 0)))
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=(0, 20))
    
    def _plot_performance_comparison(self, ax):
        ax.set_facecolor('#1E1E1E')
        
        algorithms = list(self.results.keys())
        clean_names = [name.split(' ', 1)[1] for name in algorithms]
        
        avg_scores = [self.results[algo]['avg'] for algo in algorithms]
        max_scores = [self.results[algo]['max'] for algo in algorithms]
        
        x = np.arange(len(clean_names))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, avg_scores, width, label='Average Score', 
                      color='#3498db', alpha=0.8)
        bars2 = ax.bar(x + width/2, max_scores, width, label='Max Score',
                      color='#2ecc71', alpha=0.8)
        
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{int(height)}',
                          xy=(bar.get_x() + bar.get_width() / 2, height),
                          xytext=(0, 3),
                          textcoords="offset points",
                          ha='center', va='bottom',
                          color='white', fontsize=8)
        
        autolabel(bars1)
        autolabel(bars2)
        
        ax.set_title('Performance Comparison', color='white', pad=20, fontsize=16)
        ax.set_xticks(x)
        ax.set_xticklabels(clean_names, rotation=45, ha='right')
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', framealpha=0.8)
        ax.grid(True, alpha=0.2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    def _plot_algorithm_rankings(self, ax):
        ax.set_facecolor('#1E1E1E')
        
        # Find global maximum score for fair comparison
        global_max_score = max(
            max(data['scores'])
            for data in self.results.values()
        )
        
        # Calculate algorithm scores
        algorithm_scores = []
        for algo in self.results.keys():
            data = self.results[algo]
            avg_score = data['avg']
            max_score = data['max']
            
            # Calculate consistency based on coefficient of variation
            cv = data['std'] / (avg_score if avg_score > 0 else 1)
            consistency = 1 - min(cv, 1)  # Cap at 1 to prevent negative scores
            
            # Calculate overall score using global maximum
            overall_score = (
                0.5 * (avg_score / global_max_score) +  # Increased weight on actual performance
                0.3 * (max_score / global_max_score) +  # Slightly reduced weight on max score
                0.2 * consistency                       # Keep consistency weight
            ) * 100
            
            algorithm_scores.append({
                'name': algo.split(' ', 1)[1],
                'score': overall_score,
                'avg_score': avg_score,
                'max_score': max_score,
                'consistency': consistency * 100
            })
        
        algorithm_scores.sort(key=lambda x: x['score'], reverse=True)
        
        names = [score['name'] for score in algorithm_scores]
        scores = [score['score'] for score in algorithm_scores]
        
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f1c40f', '#9b59b6', 
                 '#1abc9c', '#e67e22', '#34495e', '#7f8c8d', '#c0392b']
        
        bars = ax.barh(np.arange(len(names)), scores, 
                      color=[colors[i % len(colors)] for i in range(len(names))],
                      alpha=0.8)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                   f'{scores[i]:.1f}%',
                   va='center', color='white')
        
        ax.set_title('Algorithm Rankings', color='white', pad=20, fontsize=16)
        ax.set_yticks(np.arange(len(names)))
        ax.set_yticklabels(names)
        ax.set_xlim(0, 105)
        ax.grid(True, alpha=0.2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        criteria_text = "Ranking Criteria:\n" + \
                       "• 50% Average Score\n" + \
                       "• 30% Max Score\n" + \
                       "• 20% Consistency"
        
        props = dict(boxstyle='round', facecolor='#2C3E50', alpha=0.8)
        ax.text(1.02, 0.02, criteria_text,
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment='bottom',
                bbox=props)
    
    def _create_save_button(self, container):
        save_button = ctk.CTkButton(
            container,
            text="💾 Save Results",
            font=ctk.CTkFont(size=14),
            command=self._save_results,
            width=150,
            height=35
        )
        save_button.pack(pady=10)
    
    def _save_results(self):
        if not os.path.exists('simulation_results'):
            os.makedirs('simulation_results')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"simulation_results/snake_simulation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4) 