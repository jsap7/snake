from .astar import AStarAI
from .bfs import BFSAI
from .dfs import DFSAI
from .advanced_hamiltonian import AdvancedHamiltonianAI
from .hybrid import HybridAI
from .random_walk import RandomWalkAI
from .greedy import GreedyBestFirstAI

# Dictionary mapping algorithm names to their classes
AI_ALGORITHMS = {
    "astar": AStarAI,
    "bfs": BFSAI,
    "dfs": DFSAI,
    "advanced_hamiltonian": AdvancedHamiltonianAI,
    "hybrid": HybridAI,
    "random": RandomWalkAI,
    "greedy": GreedyBestFirstAI
}
