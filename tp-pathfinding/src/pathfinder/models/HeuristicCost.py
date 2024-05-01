from src.pathfinder.models.node import Node
from src.pathfinder.models.grid import Grid

def HeuristicCost(grid: Grid, node: Node) -> int:
    return(sum(map(lambda x, y: abs(x - y), grid.end, node.state)))
