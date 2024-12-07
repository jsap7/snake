from .astar import AStarAI
from .bfs import BFSAI
from .dijkstra import DijkstraAI
from .greedy import GreedyBestFirstAI
from .hamiltonian import HamiltonianWithShortcutsAI
from .hybrid import HybridAI
from .random_walk import RandomWalkAI
from .smart_hybrid import SmartHybridAI
from .reverse_astar import ReverseAStarAI
from .smarter_hybrid import SmarterHybridAI

AI_ALGORITHMS = {
    "astar": AStarAI,
    "bfs": BFSAI,
    "advanced_hamiltonian": HamiltonianWithShortcutsAI,
    "hybrid": HybridAI,
    "random": RandomWalkAI,
    "greedy": GreedyBestFirstAI,
    "dijkstra": DijkstraAI,
    "smart_hybrid": SmartHybridAI,
    "reverse_astar": ReverseAStarAI,
    "smarter_hybrid": SmarterHybridAI
} 