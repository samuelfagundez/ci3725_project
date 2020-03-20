import sys
from copy import deepcopy
from time import sleep
from PyQt5.QtWidgets import QApplication
from Interfaz import window
import os

# Dependiendo de la modalidad, el siguiente paso sucede automaticamente o manualmente
def waitModalidad(mod, segundos, mundo):
    # Si la modalidad es manual
    if mod:
        buildGUI(21474, mundo)
    # Si la modalidad es automatica, con un numero de segundos mayor a 0
    elif not mod and segundos > 0:
        buildGUI(segundos, mundo)

# Construye la visualizacion del mundo
def buildGUI(segundos, mundo):
    aplicacion = QApplication(sys.argv)
    ventana = window(segundos, mundo)
    ventana.show()
    if aplicacion.exec_():
        return

# Programa principal que llamara a la funcion recursiva para correr la tarea
def execute(list_of_tasks, list_of_world, list_of_instr, tarea_exe, mod, segundos):
    for tarea in list_of_tasks:
        # Si la tarea no esta en la lista de tareas a ejecutar, entonces la tarea no se ejecuta
        if tarea.getId() != tarea_exe:
            continue
        # Obtenemos el AST de la tarea
        arbol = tarea.getAST()
        # Obtenemos el mundo donde opera la tarea
        for w in list_of_world:
            if w.getId() == tarea.getWorldId():
                mundo = deepcopy(w)
                break

        # Ejecuta la tarea sobre una instancia del mundo
        execute_recursive(arbol, mundo, list_of_instr, mod, segundos)
        final_goal = mundo.getFinalGoal()
        if success_condition(final_goal, mundo):
           print("SUCCESS!")
        else:
           print("FAILED!")

        buildGUI(21474, mundo)


def success_condition(final_goal, mundo):
    if type(final_goal) is not tuple:
        # Si el goal es un booleano definido en el mundo, buscamos su valor
        goal = mundo.getBoolean(final_goal)
        if type(goal) is bool:
            return goal
        # Si no es un booleano definido, entonces es un goal definido en el mundo y verificamos si se cumple
        goal = mundo.getGoal(final_goal)
        # Si el objetivo es del tipo posicion de Willy
        if goal[0] == 0:
            return (goal[1] == mundo.getWillyPos()[0]) and (goal[2] == mundo.getWillyPos()[1])
        # Si el objetivo es del tipo objeto en bolsa de Willy
        elif goal[0] == 1:
            return goal[1] == mundo.getNumOfObjectInBasket(goal[2]) 
        # Si el objetivo es del tipo objeto en casillo
        elif goal[0] == 2:
            return goal[1] == mundo.getNumOfObjectInCell(goal[2], goal[3], goal[4])

    elif type(final_goal) is tuple:
        # Si la condicion tiene una conjuncion
        if final_goal[0] == "and":
            return success_condition(final_goal[1], mundo) and success_condition(final_goal[2], mundo)
        # Si la condicion tiene una conjuncion
        elif final_goal[0] == "or":
            return (success_condition(final_goal[1], mundo) or success_condition(final_goal[2], mundo))
        # Si la condicion tiene un negado
        elif final_goal[0] == "not":
            return not success_condition(final_goal[1], mundo)



def condition_recursive(cond, mundo):
    if type(cond) is not tuple:
        # Si la condicion es que willy este viendo direccion norte
        if cond == "looking-north":
            if mundo.getWillyPos()[2] == "north":
                return True
            return False
        # Si la condicion es que willy este viendo direccion norte
        elif cond == "looking-east":
            if mundo.getWillyPos()[2] == "east":
                return True
            return False
        # Si la condicion es que willy este viendo direccion norte
        elif cond == "looking-south":
            if mundo.getWillyPos()[2] == "south":
                return True
            return False
        # Si la condicion es que willy este viendo direccion norte
        elif cond == "looking-west":
            if mundo.getWillyPos()[2] == "west":
                return True
            return False
        # Si la condicion es que la casilla del frente no tenga pared
        elif cond == "front-clear":
            pos = mundo.getWillyPos()
            return not mundo.isWallInCell(pos[0], pos[1], pos[2])
        # Si la condicion es que la casilla de la izquierda no tenga pared
        elif cond == "left-clear":
            pos = mundo.getWillyPos()
            if pos[2] == "north":
                return not mundo.isWallInCell(pos[0], pos[1], "west")
            elif pos[2] == "east":
                return not mundo.isWallInCell(pos[0], pos[1], "north")
            elif pos[2] == "south":
                return not mundo.isWallInCell(pos[0], pos[1], "east")
            elif pos[2] == "west":
                return not mundo.isWallInCell(pos[0], pos[1], "south")
        # Si la condicion es que la casilla de la derecha no tenga pared
        elif cond == "right-clear":
            pos = mundo.getWillyPos()
            if pos[2] == "north":
                return not mundo.isWallInCell(pos[0], pos[1], "east")
            elif pos[2] == "east":
                return not mundo.isWallInCell(pos[0], pos[1], "south")
            elif pos[2] == "south":
                return not mundo.isWallInCell(pos[0], pos[1], "west")
            elif pos[2] == "west":
                return not mundo.isWallInCell(pos[0], pos[1], "north")
        # Si la condicion es un literal booleano 
        elif type(cond) is bool:
            return cond
        # Si la condicion es un booleano definido en el mundo
        else:
            return mundo.getBoolean(cond)

    elif type(cond) is tuple:
        # Si la condicion tiene una conjuncion
        if cond[0] == "and":
            return condition_recursive(cond[1], mundo) and condition_recursive(cond[2], mundo)
        # Si la condicion tiene una conjuncion
        elif cond[0] == "or":
            return condition_recursive(cond[1], mundo) or condition_recursive(cond[2], mundo)
        # Si la condicion tiene un negado
        elif cond[0] == "not":
            return not condition_recursive(cond[1], mundo)
        # Si la condicion es revisar si willy carga un tipo de objeto en la bolsa
        elif cond[0] == "carrying":
            if mundo.getNumOfObjectInBasket(cond[1]) > 0:
                return True
            return False
        # Si la condicion es revisar si existe un objeto en especifico en la casilla donde se encuentra willy
        elif cond[0] == "found":
            if mundo.getNumOfObjectInCell(cond[1], mundo.getWillyPos()[0], mundo.getWillyPos()[1]) > 0:
                return True
            return False


def execute_recursive(nodo, mundo, list_of_instr, mod, segundos):
    if type(nodo) is not tuple:
        # Mueve a willy una casilla en la direccion que esta mirando 
        if nodo == "move":
            pos = mundo.getWillyPos()
            waitModalidad(mod, segundos, mundo)
            # Si no existe una pared al frente de willy, se mueve
            if not mundo.isWallInCell(pos[0], pos[1], pos[2]):
                mundo.move()
            else:
                print("Error: Willy no puede moverse a casillas con una pared o fuera de los bordes del mundo.")
                sys.exit(0)
        # Willy voltea a la izquierda
        elif nodo == "turn-left":
            waitModalidad(mod, segundos, mundo)
            pos = mundo.getWillyPos()
            if pos[2] == "north":
                mundo.willyPos[2] = "west"
            elif pos[2] == "east":
                mundo.willyPos[2] = "north"
            elif pos[2] == "south":
                mundo.willyPos[2] = "east"
            elif pos[2] == "west":
                mundo.willyPos[2] = "south"

        # Willy voltea a la derecha
        elif nodo == "turn-right":
            waitModalidad(mod, segundos, mundo)
            pos = mundo.getWillyPos()
            if pos[2] == "north":
                mundo.willyPos[2] = "east"
            elif pos[2] == "east":
                mundo.willyPos[2] = "south"
            elif pos[2] == "south":
                mundo.willyPos[2] = "west"
            elif pos[2] == "west":
                mundo.willyPos[2] = "north"
        # Termina la ejecucion del programa
        elif nodo == "terminate":
            return True
        # Llamada a una instruccion definida por el usuario
        else:
            if nodo is None:
                return
            # Obtenemos el num de bloque de la instruccion
            nodo = nodo.split(" | ")
            # Buscamos la instruccion con ese num de bloque
            for instr in list_of_instr:
                # Si la encontramos, entonces ejecutamos su arbol de instrucciones
                if instr.getBloqNum() == int(nodo[1]):
                    execute_recursive(instr.getInstr(), mundo, list_of_instr, mod, segundos)
                    break

    elif type(nodo) is tuple:
        # Recoge un objeto de la celda
        if nodo[0] == "pick":
            waitModalidad(mod, segundos, mundo)
            mundo.placeInBasket(1,nodo[1])
            pos = mundo.getWillyPos()
            mundo.world[pos[0]-1][pos[1]-1].pickObjeto(nodo[1])

        # Deja un objeto en la celda actual
        elif nodo[0] == "drop":
            waitModalidad(mod, segundos, mundo)
            pos = mundo.getWillyPos()
            mundo.world[pos[0]-1][pos[1]-1].setObjeto(nodo[1], 1)
            mundo.objetos[nodo[1]] -= 1
            if mundo.objetos[nodo[1]] == 0:
                del self.objetos[nodo[1]]

        # Cambia el valor de un booleano a True o a el indicado por el usuario
        elif nodo[0] == "set":
            # Si la instruccion es "set... to..."
            if len(nodo) == 4:
                mundo.setBoolean(nodo[1], nodo[3])
            # Si la instruccion es "set..."
            else:
                mundo.setBoolean(nodo[1], True)

        # Cambia el valor de un booleano a False
        elif nodo[0] == "clear":
            mundo.setBoolean(nodo[1], False)

        # Complementa el valor de un Booleano
        elif nodo[0] == "flip":
            mundo.setBoolean(nodo[1], not mundo.getBoolean(nodo[1]))

        # Repite una instruccion un numero acotado de veces
        elif nodo[0] == "repeat":
            for i in range(int(nodo[1])):
                terminate = execute_recursive(nodo[2], mundo, list_of_instr, mod, segundos)
                # Si se detuvo la ejecucion del programa
                if terminate is not None:
                    return True
        
        # Si la instruccion es una instruccion if
        elif nodo[0] == "if":
            terminate = None
            # Si la condicion es verdadera, ejecutamos la instruccion en if
            if condition_recursive(nodo[1], mundo):
                terminate = execute_recursive(nodo[2], mundo, list_of_instr, mod, segundos)
            # Si la condicion es falsa y la instruccion es "if... else...", ejecutamos la instruccion en else
            elif len(nodo) == 5:
                terminate = execute_recursive(nodo[4], mundo, list_of_instr, mod, segundos)
            # Si se detuvo la ejecucion del programa
            if terminate is not None:
                return True
        
        # Si la instruccion es un ciclo while
        elif nodo[0] == "while":
            while condition_recursive(nodo[1], mundo):
                terminate = execute_recursive(nodo[2], mundo, list_of_instr, mod, segundos)
                # Si se detuvo la ejecucion del programa
                if terminate is not None:
                    return True
        
        # Si la instruccion es una instruccion compuesta
        elif nodo[0] == "begin":
            terminate = execute_recursive(nodo[1], mundo, list_of_instr, mod, segundos)
            # Si se detuvo la ejecucion del programa
            if terminate is not None:
                return True

        # Recorre a los hijos del nodo
        else:
            for n in nodo:
                terminate = execute_recursive(n, mundo, list_of_instr, mod, segundos)
                # Si se detuvo la ejecucion del programa
                if terminate is not None:
                    return True