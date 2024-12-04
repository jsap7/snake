from .astar import AStarAI
from .bfs import BFSAI
from .dfs import DFSAI
from .hamiltonian import HamiltonianWithShortcutsAI
from .random_walk import RandomAI

# Dictionary mapping algorithm names to their classes
AI_ALGORITHMS = {
    "astar": AStarAI,
    "bfs": BFSAI,
    "dfs": DFSAI,
    "hamiltonian": HamiltonianWithShortcutsAI,
    "random": RandomAI
}
