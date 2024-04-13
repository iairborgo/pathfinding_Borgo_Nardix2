from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from ..models.HeuristicCost import HeuristicCost

class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        
        frontier = PriorityQueueFrontier()
        frontier.add(node, HeuristicCost(grid, node))

        while frontier: # Mientras haya  nodos en la frontera
            node = frontier.pop()
            if grid.end == node.state: return Solution(node, explored)
            for accion, vecino in grid.get_neighbours(node.state).items():
                costo_total = node.cost + grid.get_cost(vecino)
                if vecino not in explored or costo_total < explored[vecino]:
                    new_node = Node("", vecino, costo_total, node, accion)
                    explored[vecino] = costo_total
                    frontier.add(new_node, priority = HeuristicCost(grid,new_node))

        return NoSolution(explored) # Significa que no hay mas nodos que explorar y no se llego a una sol
