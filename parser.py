import ply.yacc as yacc
from lexer import tokens
from World import World
from Task import Task
import sys


# Lista de mundos definidos
list_of_world = []
# Lista de tareas definidas
list_of_tasks = []
# Tarea actual que se esta definiendo. Sera una instancia de la clase Task
current_task = None
# Mundo actual que se esta definiendo. Sera una instancia de la clase world
current_world = None
# Son ordenados de menor a mayor precedencia
precedence = (
    ('left', 'TkAnd'),
    ('left', 'TkOr'),
    ('right', 'TkNot')
)

# Checkea si el identificador esta siendo utilizado para definir un mundo ya definido. Devuelve
# True si esto sucede y False si no sucede


def checkExistingWorldId(id):
    for i in range(len(list_of_world)):
        if id == list_of_world[i].getWorldId():
            return True
    return False

# Checkea si el identificador esta siendo utilizado para definir una tarea ya definido. Devuelve
# True si esto sucede y False si no sucede


def checkExistingTaskId(id):
    for i in range(len(list_of_tasks)):
        if id == list_of_tasks[i].getId():
            return True
    return False


# la regla gramatica inicial es la funcion mas arriba en el archivo, aqui es donde el parser debe llegar y
# una vez que llega se detiene y regresa el valor en p[0]. Si el parser no llega aqui, se da un syntax error.

def p_program(p):
    '''program : program world
               | program task
               | world
               | task'''


def p_world(p):
    '''world : beginworld instruccionesWorld TkEndWorld'''
    global current_world, list_of_world

    list_of_world.append(current_world)
    current_world = None


# Inicializa un nuevo mundo. Esto se hace primero ya que necesitamos crear la instancia de World
# para irla llenando mientras se realiza el parseo
def p_beginworld(p):
    '''beginworld : TkBeginWorld term_id'''
    global current_world
    if checkExistingWorldId(p[2]):
        print("Error de sintaxis: No se puede utilizar un mismo identificador para definir dos mundos distintos.")
        sys.exit(0)

    current_world = World(p[2])


def p_instruccionesWorld(p):
    '''instruccionesWorld : instruccionesWorld instruccionWorld TkSemiColon
                          | instruccionWorld TkSemiColon'''


# Intruccion World
def p_instruccion_World(p):
    '''instruccionWorld : TkWorld term_num term_num'''
    global current_world
    q = current_world.newWorld(p[2], p[3])
    if q != True:
        # Los mensaje de error no seran asi, esperar a German a que lo pase!!!!!!!
        print("Error de sintaxis: World " + str(p[1]) + q)
        sys.exit(0)


# Intruccion Wall
def p_instruccion_Wall(p):
    '''instruccionWorld : TkWall term_dir TkFrom term_num term_num TkTo term_num term_num'''
    global current_world
    q = current_world.newWall(p[2], p[4], p[5], p[7], p[8])
    if q != True:
        print("Error de sintaxis: Wall " + q)
        sys.exit(0)


# Intruccion Object-type
def p_instruccion_Object_type(p):
    '''instruccionWorld : TkObjectType term_id TkOfColor term_color'''
    global current_world
    q = current_world.newObject(p[2], p[4])
    if q != True:
        print("Error de sintaxis: Object-type" + q)
        sys.exit(0)


# Intruccion Place en casilla
def p_instruccion_Place_casilla(p):
    '''instruccionWorld : TkPlace term_num TkOf term_id TkAt term_num term_num'''
    global current_world
    q = current_world.placeInWorld(p[2], p[4], p[6], p[7])
    if q != True:
        print("Error de sintaxis: Place in " + q)
        sys.exit(0)


# Intruccion Place en bolsa
def p_instruccion_Place_in_basket(p):
    '''instruccionWorld : TkPlace term_num TkOf term_id TkInBasket'''
    global current_world
    q = current_world.placeInBasket(p[2], p[4])
    if q != True:
        print("Error de sintaxis: Place in basket " + q)
        sys.exit(0)


# Intruccion Start de willy
def p_instruccion_Start_willy(p):
    '''instruccionWorld : TkStartAt term_num term_num TkHeading term_dir'''
    global current_world
    q = current_world.willyStartAt(p[2], p[3], p[5])
    if q != True:
        print("Error de sintaxis: Start At " + q)
        sys.exit(0)


# Intruccion Basket of capacity
def p_instruccion_Basket_capacity(p):
    '''instruccionWorld : TkBasketOfCapacity term_num'''
    global current_world
    q = current_world.setCapacityOfBasket(p[2])
    if q != True:
        print("Error de sintaxis: Basket of capacity " + q)
        sys.exit(0)


# Intruccion que define Booleano
def p_instruccion_Boolean(p):
    '''instruccionWorld : TkBoolean term_id TkWithInitialValue term_bool'''
    global current_world
    q = current_world.newBoolean(p[2], p[4])
    if q != True:
        print("Error de sintaxis: Boolean " + q)
        sys.exit(0)


# Intruccion Goal
def p_instruccion_Goal(p):
    '''instruccionWorld : TkGoal term_id TkIs TkWillyIsAt term_num term_num
                        | TkGoal term_id TkIs term_num term_id TkObjectsInBasket
                        | TkGoal term_id TkIs term_num term_id TkObjectsAt term_num term_num'''
    global current_world
    if p[4] == "willy is at":
        q = current_world.setGoalPosWilly(p[2], p[5], p[6])
    elif p[6] == "objects in Basket":
        q = current_world.setGoalObjBasket(p[2], p[4], p[5])
    elif p[6] == "objects at":
        q = current_world.setGoalObjCelda(p[2], p[4], p[5], p[7], p[8])
    if q != True:
        print("Error de sintaxis: Goal " + q)
        sys.exit(0)


# Instruccion de el Objetivo Final. Esto puede cambiar, creo que no se hace asi !!!!!!!!
def p_instruccion_Final_goal(p):
    '''instruccionWorld : TkFinalGoalIs condicionGoal'''
    global current_world
    q = current_world.setFinalGoal(p[2])
    if q != True:
        print("Error de sintaxis: Final goal is " + q)
        sys.exit(0)


# Define la condicion para que el programa sea exitoso. Esto puede cambiar, creo que no se hace asi !!!!!!!!!!!!!!!!
def p_condicion_Goal(p):
    '''condicionGoal : condicionGoal TkAnd condicionGoal
                     | condicionGoal TkOr condicionGoal
                     | TkNot condicionGoal
                     | TkLParen condicionGoal TkRParen
                     | term_id'''

    if len(p) == 4:
        if (p[2] == "and"):
            p[0] = p[1] + "and " + p[3]

        elif p[2] == "or":
            p[0] = p[1] + "or " + p[3]

        elif (p[1] == "(") and (p[3] == ")"):
            p[0] = "(" + p[2] + ") "

    else:
        if p[1] == "not":
            p[0] = "not " + p[2]

        else:
            p[0] = p[1] + " "


################################################
#                     Task                     #
################################################

# Crea el nuevo task y lo agrega a la lista de tasks
def p_task(p):
    '''task : begintask instruccionesTask TkEndTask
            | begintask TkEndTask'''
    global current_task, list_of_tasks

    if len(p) == 4:
        print(p[2])
        current_task.setArbolRecursivoInstr(p[2])
        list_of_tasks.append(current_task)
    current_task = None


# Inicializa un nuevo task. Esto se hace primero ya que necesitamos crear la instancia de Task
# para irla llenando mientras se realiza el parseo
def p_begintask(p):
    '''begintask : TkBeginTask term_id TkOn term_id'''
    global current_task

    # Como no puede haber una tarea con el mismo identificador de un mundo
    # ni dos tareas con el mismo identificador. Se deben checkear los dos
    if checkExistingTaskId(p[2]):
        print("Error de sintaxis: No se puede utilizar un mismo identificador para definir dos tareas distintas.")
        sys.exit(0)
    if checkExistingWorldId(p[2]):
        print("Error de sintaxis: No se puede utilizar un mismo identificador para definir una tarea y un mundo.")
        sys.exit(0)
    # Checkea si la tarea esta siendo definida sobre un mundo que existe
    if not checkExistingWorldId(p[4]):
        print(
            "Error de sintaxis: No se puede definir una tarea sobre un mundo no existente.")

    current_task = Task(p[2], p[4])


# Reduce las instrucciones
def p_instruccionesTask(p):
    '''instruccionesTask : instruccionesTask instruccionTask TkSemiColon
                         | instruccionTask TkSemiColon'''

    if len(p) == 4:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]


def p_instruccion_if(p):
    '''instruccionTask : TkIf term_bool TkThen instruccionTask'''

    p[0] = (p[1], p[2], p[4])


def p_instruccion_primitiva_move(p):
    '''instruccionTask : TkMove'''

    p[0] = p[1]


def p_instruccion_primitiva_turn_left(p):
    '''instruccionTask : TkTurnLeft'''

    p[0] = p[1]


def p_instruccion_primitiva_turn_right(p):
    '''instruccionTask : TkTurnRight'''

    p[0] = p[1]


def p_instruccion_primitiva_pick(p):
    '''instruccionTask : TkPick term_id'''

    p[0] = (p[1], p[2])


def p_instruccion_primitiva_drop(p):
    '''instruccionTask : TkDrop term_id'''

    p[0] = (p[1], p[2])


def p_instruccion_primitiva_set(p):
    '''instruccionTask : TkSet term_id TkTo term_bool 
                    | TkSet term_id'''

    if len(p) == 5:
        p[0] = (p[1], p[2], p[4])
    else:
        p[0] = (p[1], p[2])


def p_instruccion_primitiva_clear(p):
    '''instruccionTask : TkClear term_id'''

    p[0] = (p[1], p[2])


def p_instruccion_primitiva_flip(p):
    '''instruccionTask : TkFlip term_id'''

    p[0] = (p[1], p[2])


def p_instruccion_primitiva_terminate(p):
    '''instruccionTask : TkTerminate'''

    p[0] = p[1]


# Terminal numero {0,1,...,9}
def p_term_num(p):
    '''term_num : TkNum'''
    p[0] = p[1]

# Terminal Booleano {true, false}


def p_term_bool(p):
    '''term_bool : TkTrue
                 | TkFalse'''
    p[0] = p[1]

# Terminal Identificador


def p_term_id(p):
    '''term_id : TkId'''
    p[0] = p[1]

# Terminal direccion {north, south, east, west}


def p_term_dir(p):
    '''term_dir : TkNorth
                | TkSouth
                | TkEast
                | TkWest'''
    p[0] = p[1]

# Terminal color {red, blue, magenta, cyan, green, or yellow}


def p_term_color(p):
    '''term_color : TkRed
                  | TkBlue
                  | TkMagenta
                  | TkCyan
                  | TkGreen
                  | TkYellow'''
    p[0] = p[1]


# def p_test_and(p):
#    '''test : test TkAnd term_bool '''
#    p[0] = p[1] and p[3]

# def p_test_or(p):
#    '''test : test TkOr term_bool '''
#    p[0] = p[1] or p[3]

# def p_test_not(p):
#    '''test : TkNot test'''
#    p[0] = not p[2]

# def p_test_term_bool(p):
#    '''test : term_bool'''
#    p[0] = p[1]


# Regla para los errores de Sintaxis
def p_error(p):
    print("Syntax error in input!")
    sys.exit(0)


# Construye el parser
parser = yacc.yacc()


try:
    fp = open("prueba.txt", "r")
    s = fp.read()
except EOFError:
    pass
result = parser.parse(s)
print(result)
