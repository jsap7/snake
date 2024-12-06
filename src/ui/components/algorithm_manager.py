import customtkinter as ctk
import logging

class AlgorithmManager:
    def __init__(self, parent, algorithm_var):
        self.parent = parent
        self.algorithm_var = algorithm_var
        self.radio_buttons = []
        
        # Default algorithms list
        self.algorithms = [
            ("🎯 A* Pathfinding", "astar", "Optimal path finding to food"),
            ("🌊 BFS Pathfinding", "bfs", "Breadth-first search for shortest path"),
            ("🔄 Advanced Hamiltonian", "advanced_hamiltonian", "Optimized safe path"),
            ("🤖 Hybrid A*/Hamiltonian", "hybrid", "Adaptive strategy switching"),
            ("🔍 DFS Exploration", "dfs", "Depth-first exploration"),
            ("🎲 Random Walk", "random", "Random valid moves"),
            ("⚡ Greedy Best-First", "greedy", "Always moves towards food"),
            ("🌐 Dijkstra", "dijkstra", "Finds shortest path by exploring all directions"),
            ("🧱 Wall Follower", "wall_follower", "Follows walls and edges of the grid"),
            ("🎮 Smart Hybrid", "smart_hybrid", "Combines A* and Wall Following adaptively"),
            ("🧬 Genetic Algorithm", "genetic", "Evolves behavior through generations"),
            ("🌟 Perfect AI", "perfect", "Combines A* with Hamiltonian cycle and safe shortcuts"),
            ("🔄 Reverse A*", "reverse_astar", "Finds longest valid path to food"),
        ]
        
        self.algorithms_scroll = None
        self._create_algorithm_list()
    
    def _create_algorithm_list(self):
        """Create the scrollable algorithm list"""
        self.algorithms_scroll = ctk.CTkScrollableFrame(
            self.parent,
            height=350,
            width=600
        )
        self.algorithms_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        for text, value, desc in self.algorithms:
            self._add_algorithm_button(text, value, desc)
    
    def _add_algorithm_button(self, text, value, desc):
        """Add a new algorithm radio button"""
        frame = ctk.CTkFrame(self.algorithms_scroll)
        frame.pack(fill="x", pady=5)
        
        radio = ctk.CTkRadioButton(
            frame,
            text=text,
            variable=self.algorithm_var,
            value=value,
            font=ctk.CTkFont(size=14),
            width=200
        )
        radio.pack(side="left", padx=10)
        
        desc_label = ctk.CTkLabel(
            frame,
            text=desc,
            font=ctk.CTkFont(size=12),
            wraplength=350,
            justify="left"
        )
        desc_label.pack(side="left", padx=(5, 10), fill="x", expand=True)
        self.radio_buttons.append(radio)
    
    def add_trained_model(self, timestamp, fitness):
        """Add a trained model to the algorithm list"""
        new_algo = (
            f"🧠 Trained GA {timestamp}", 
            f"trained_ga_{timestamp}", 
            f"Trained genetic algorithm (fitness: {fitness:.0f})"
        )
        self.algorithms.append(new_algo)
        self._add_algorithm_button(*new_algo)
        return new_algo
    
    def set_buttons_state(self, state):
        """Enable/disable all algorithm buttons"""
        for radio in self.radio_buttons:
            radio.configure(state=state)
    
    def get_algorithm_by_id(self, algo_id):
        """Get algorithm tuple by its ID"""
        return next((algo for algo in self.algorithms if algo[1] == algo_id), None) 