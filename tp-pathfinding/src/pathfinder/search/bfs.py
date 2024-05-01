from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:

        node = Node("", state=grid.start, cost=0, parent=None, action=None) # Inicio Nodo en posicion de inicio

        reached = {}                        # Diccionario de alcanzados
        reached[node.state] = True          # Estado inicial del diccionario

        if node.state == grid.end:
            return Solution(node, reached)  # Chequeo si está en un estado objetivo
        
        frontier = QueueFrontier()
        frontier.add(node)                  # Inicio frontera con el nodo inicial (Tipo cola)

        while True:

            if frontier.is_empty():
                return NoSolution(reached)  

            node = frontier.remove()   

            successors = grid.get_neighbours(node.state) # Vecinos del nodo actual

            directions = ['right', 'up', 'down', 'left'] # Posibles movimientos

            for direction in directions: 
                if direction in successors:
                    new_state = successors[direction]   # Si es válida obtiene el nuevo estado moviendose en esa direccion
                    if new_state not in reached:        
                        new_node = Node("", new_state,
                                        node.cost + grid.get_cost(new_state),
                                        parent=node, action=direction)  # Si ese estado aun no fue alcanzado, creo el nuevo nodo para el nuevo estado
                        reached[new_state] = True       # Alcanzado
                        if new_state == grid.end:
                            return Solution(new_node, reached)
                        frontier.add(new_node)          # Agrego el nuevo nodo