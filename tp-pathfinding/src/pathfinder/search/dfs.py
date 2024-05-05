from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", state=grid.start, cost=0, parent=None, action=None)

        # Initialize the reached dictionary with the initial state
        explored = {}
        explored[node.state] = True

        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, explored)
        
        # Initialize the frontier with the initial node
        # In this example, the frontier is a Stack
        frontier = StackFrontier()
        frontier.add(node)
        
        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)
            
            # Remove a node from the frontier
            node = frontier.remove()

            # DFS
            # Initialize the successors with the neighbours
            successors = grid.get_neighbours(node.state)
            # Initialize the possible directions
            directions = ['right', 'up', 'down', 'left']

            for direction in directions:
                if direction in successors: 
                    # Initialize a new state
                    new_state = successors[direction]
                    if new_state not in explored:
                        # If the new state is not explored yet, create a new node
                        new_node = Node("", new_state,
                                        node.cost + grid.get_cost(new_state),
                                        parent=node, action=direction)
                        # Add the new state to explored
                        explored[new_state] = True
                        # If is an objective state, return the solution
                        if new_state == grid.end:
                            return Solution(new_node, explored)
                        # Add the new node to the frontier
                        frontier.add(new_node)