"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem
from random import choice
from time import time


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            else:

                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas con reinicio aleatorio.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local. Una vez alcanzado, se reinicia
    con un estado aleatorio hasta alcanzar las n iteraciones y retorna la mejor.
    """
    def solve(self, problem: OptProblem, iters : int = 10):
        start = time()  # inicia el contador

        i = 0

        while i < iters: # Iniciamos aleatoriamente n veces
            actual = problem.random_reset()
            value = problem.obj_val(actual)
            
            while True:
                diff = problem.val_diff(actual) # Determinamos las acciones y sus costos
                # y agarramos las que nos dan mayor valor objetivo
                max_acts = [act for act, val in diff.items() if val == max(diff.values())]

                act = choice(max_acts) # Elige una aleatoria entre las anteriores

                if diff[act] <= 0: # si no hay mejor movimiento para hacer:
                    i += 1
                    # int < None da typeerror
                    if self.value == None: # si todavia no hay ninguno guardado lo guardamos
                        self.tour = actual
                        self.value = value
                    elif self.value < value: # o guardamos el nuevo camino si tiene mejor costo
                        self.tour = actual   # que el anterior que teniamos
                        self.value = value
                    break # rompemos el while true ya que encontramos la sol de la iteracion
                else:
                    actual = problem.result(actual, act)
                    value = value + diff[act]
                    self.niters += 1                      
                    
                
        end = time()
        self.time = end-start
        return

 

class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con busqueda tabu.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        mejor = actual # Se inicia el mejor como el estado inicial

        lista_tabu = []

        while self.niters < 50: # Elijo máximo de iteraciones como criterio de parada

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)         # Veo cuales son todas las posibles diferencias que se generan

            max_diff = max(diff.values())           # Defino cual es la mayor diferencia de valor objetivo que se puede lograr, aplicando algunas de las acciones disponibles

            # Buscar las acciones que generan el mayor incremento de valor obj Y NO ESTEN EN LISTA TABU
            max_acts = [act for act, val in diff.items() if val == max_diff and act not in lista_tabu] 
            
            if not max_acts:
                max_acts = [act for act, val in diff.items() if val == max_diff]    # Si no hay acciones que mejoren el Valor Objetivo
            
            act = choice(max_acts) # Si no existe ninguno que no esté en la lista tabu agarra alguno que maximice

            if problem.obj_val(mejor) < problem.obj_val(actual): # Si el actual es mejor que el mejor lo actualizamos
                mejor = actual

            lista_tabu.append(act) # Actualizo lista tabu

            if len(lista_tabu) > 10: # Limite de tamaño de lista tabu
                lista_tabu.pop(0)

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if max_diff <= 0:
                end = time()
                self.time = end - start
                self.tour = actual
                self.value = value
                return
            
            # Sino, nos movemos al sucesor
            else:
                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1
