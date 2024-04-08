from ..models.grid import Grid
from ..models.frontier import StackFrontier, PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {}
        explored[node.state] = True

        # Creamos la frontera

        frontier = PriorityQueueFrontier()
        frontier.add(node, priority = node.cost)


        # Arrancamos a iterar
        while True:
            if frontier.is_empty(): return NoSolution(explored)
            node = frontier.pop()
            if grid.end == node.state: return Solution(node, explored)
            for accion, vecino in grid.get_neighbours(node.state).items(): # es s' en teoria
                costo_total = node.cost + grid.get_cost(vecino) # es c' en teoria
                if vecino not in explored or costo_total < explored[vecino]:
                    new_node = Node("", vecino, costo_total, node, accion)
                    explored[vecino] = costo_total
                    frontier.add(new_node, priority = costo_total)
