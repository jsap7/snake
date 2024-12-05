from .astar import AStarAI
from .bfs import BFSAI
from .dfs import DFSAI
from .dijkstra import DijkstraAI
from .greedy import GreedyBestFirstAI
from .hamiltonian import HamiltonianWithShortcutsAI
from .hybrid import HybridAI
from .random_walk import RandomWalkAI
from .smart_hybrid import SmartHybridAI
from .wall_follower import WallFollowerAI
from .genetic import GeneticAI

AI_ALGORITHMS = {
    "astar": AStarAI,
    "bfs": BFSAI,
    "dfs": DFSAI,
    "dijkstra": DijkstraAI,
    "greedy": GreedyBestFirstAI,
    "advanced_hamiltonian": HamiltonianWithShortcutsAI,
    "hybrid": HybridAI,
    "random": RandomWalkAI,
    "smart_hybrid": SmartHybridAI,
    "wall_follower": WallFollowerAI,
    "genetic": GeneticAI
}
