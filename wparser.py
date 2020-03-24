import ply.yacc as yacc
from lexer import tokens
from World import World
from Task import Task
from Tabla_simbolos import TSimbolos
from Func import Func
import sys


# Lista de mundos definidos
list_of_world = []
# Tabla de simbolos
TSimbolos = TSimbolos()
# Bloques totales del programa
bloq_num = 0
# Pila que guarda temporalmente los num. de bloques de las instrucciones a definir
func_bloq_num = []
# Lista de tareas definidas
list_of_tasks = []
# Lista de instrucciones definidas
list_of_instr = []
# Tarea actual que se esta definiendo. Sera una instancia de la clase Task
current_task = None
# Mundo actual que se esta definiendo. Sera una instancia de la clase world
current_world = None
# Variable que indica si ocurrio un error de contexto o no
e = False
# Son ordenados de menor a mayor precedencia
precedence = (
    ('left', 'TkOr'),
    ('left', 'TkAnd'),
    ('right', 'TkNot'),
    ('right', 'TkThen'),         # Se deben agregar las precedencia entre then y else para resolver 
    ('right', 'TkElse')          # shift/reduce de la instruccion if cuando hace uso de else
)

# Chequea si el identificador esta siendo utilizado para definir un mundo ya definido. Devuelve 
# True si esto sucede y False si no sucede
def checkExistingWorldId(id):
    for i in range(len(list_of_world)):
        if id == list_of_world[i].getId():
            return True
    return False

# Chequea si el identificador esta siendo utilizado para definir una tarea ya definida. Devuelve 
# True si esto sucede y False si no sucede
def checkExistingTaskId(id):
    for i in range(len(list_of_tasks)):
        if id == list_of_tasks[i].getId():
            return True
    return False

# Devuelve el numero de linea y columna del token. La usamos cuando se genera un error y necesitamos
# saber donde ocurrio
def linenoLexpos(p, n):
    return p.lineno(n), p.lexpos(n)

def checkContextError():
    return e

#########################################################################
#########################################################################
#########################################################################

def p_program(p):
    '''program : program world
               | program task
               | world
               | task'''

################################################
#                    World                     #
################################################

# Define el mundo creado
def p_world(p):
    '''world : beginworld instruccionesWorld TkEndWorld
             | beginworld TkEndWorld'''
    global current_world, list_of_world, bloq_num, e
    
    # Se aumenta el num. de bloques total del programa
    bloq_num += 1
    # Se le asigna el num. de bloque al mundo definido
    current_world.setBloqNum(bloq_num)
    # Si no se define la posicion inicial de willy, aqui le asignamos columna: 1,
    # fila: 1 y direccion: norte
    if current_world.getWillyPos() == (0, 0, 'north'):
        q = current_world.willyStartAt(1, 1, 'north')
        if q != True:
            print("\n- Error: " + q)
            e = True
    # Si no se define el objetivo final del mundo, se notifica del error
    if current_world.getFinalGoal() is None:
        print("\n- Error en linea %s, columna %s: No se puede definir un mundo sin un objetivo final." % linenoLexpos(p, 1))
        e = True

    # Se agrega el mundo definido a la lista de mundos del programa
    list_of_world.append(current_world)
    current_world = None


# Inicializa un nuevo mundo. Esto se hace primero ya que necesitamos crear la instancia de World
# para irla llenando mientras se realiza el parseo
def p_beginworld(p):
    '''beginworld : TkBeginWorld term_id'''
    global current_world, e
    # Si ya existe un mundo con este id, se devuelve un error
    if checkExistingWorldId(p[2]):
        print("\n    "+str(p[1])+" "+str(p[2]))
        print("- Error en linea %s, columna %s: No se puede utilizar un mismo identificador para definir dos mundos distintos." % linenoLexpos(p, 2))
        p[2] = p[2] + " 2"
        e = True
    # Se crea una instancia de mundo y lo guardamos en current_world
    current_world = World(p[2])


def p_instruccionesWorld(p):
    '''instruccionesWorld : instruccionesWorld instruccionWorld TkSemiColon
                          | instruccionesWorld TkSemiColon
                          | instruccionWorld TkSemiColon
                          | donothing'''


def p_do_nothing(p):
    '''donothing : TkBlockComment
                 | TkComment
                 | TkEndCBlock
                 | TkStartCBlock'''


# Intruccion World
def p_instruccion_World(p):
    '''instruccionWorld : TkWorld term_num term_num'''
    global current_world, e
    # Se crea el grid del mundo
    q = current_world.newWorld(p[2], p[3])
    # Si ocurre un error asociado a esta instruccion, se reporta
    if q != True:
        print("\n    "+str(p[1])+" "+str(p[2])+"  "+str(p[3]))
        if "filas" in q:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        else:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 1) + q)
        e = True


# Intruccion Wall
def p_instruccion_Wall(p):
    '''instruccionWorld : TkWall term_dir TkFrom term_num term_num TkTo term_num term_num'''
    global current_world, e
    # Se crea un nuevo muro
    q = current_world.newWall(p[2], p[4], p[5], p[7], p[8])
    # Si ocurre un error asociado a esta instruccion, se reporta
    if q != True:
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6])+" "+str(p[7])+" "+str(p[8]))
        if "direccion" in q:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        else:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 4) + q)
        e = True


# Intruccion Object-type
def p_instruccion_Object_type(p):
    '''instruccionWorld : TkObjectType term_id TkOfColor term_color'''
    global current_world, e
    # Se crea un nuevo tipo de objeto en el mundo actual
    q = current_world.newObject(p[2], p[4])
    # Si ocurre un error asociado a esta instruccion, se reporta
    if q != True:
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4]))
        print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        e = True


# Intruccion Place en casilla
def p_instruccion_Place_casilla(p):
    '''instruccionWorld : TkPlace term_num TkOf term_id TkAt term_num term_num'''
    global current_world, e
    # Colocamos un objeto en una casilla del mundo actual
    q = current_world.placeInWorld(p[2], p[4], p[6], p[7])
    # Si ocurre un error asociado a esta instruccion, se reporta
    if q != True:
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6])+" "+str(p[7]))
        if "numero" in q:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        elif "tipo de objeto" in q:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 4) + q)
        else:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 6) + q)
        e = True


# Intruccion Place en bolsa
def p_instruccion_Place_in_basket(p):
    '''instruccionWorld : TkPlace term_num TkOf term_id TkInBasket'''
    global current_world, e
    # Colocamos un objeto en la bolsa de willy en este mundo
    q = current_world.placeInBasket(p[2], p[4])
    # Si ocurre un error asociado a esta instruccion, se reporta
    if q != True:
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5]))
        if "tipo de objeto" in q:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 4) + q)
        else:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        e = True


# Intruccion Start de willy
def p_instruccion_Start_willy(p):
    '''instruccionWorld : TkStartAt term_num term_num TkHeading term_dir'''
    global current_world, e
    # Indicamos donde va a empezar willy en este mundo y a que direccion se dirige
    q = current_world.willyStartAt(p[2], p[3], p[5])
    # Si ocurre un error asociado a esta instruccion, se reporta
    if q != True:
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5]))
        if "instruccion" in q:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 1) + q)
        else:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        e = True


# Intruccion Basket of capacity
def p_instruccion_Basket_capacity(p):
    '''instruccionWorld : TkBasketOfCapacity term_num'''
    global current_world, e
    # Indicamos cuantos espacios tiene la bolsa de willy en este mundo
    q = current_world.setCapacityOfBasket(p[2])
    # Si ocurre un error asociado a esta instruccion, se reporta
    if q != True:
        print("\n    "+str(p[1])+" "+str(p[2]))
        if "instruccion" in q:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 1) + q)
        else:
            print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        e = True


# Intruccion que define Booleano
def p_instruccion_Boolean(p):
    '''instruccionWorld : TkBoolean term_id TkWithInitialValue term_bool'''
    global current_world, e
    # Definimos un nuevo booleano en este mundo
    q = current_world.newBoolean(p[2], p[4])
    # Si ocurre un error asociado a esta instruccion, se reporta
    if q != True:
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4]))
        print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        e = True


# Intruccion Goal
def p_instruccion_Goal(p):
    '''instruccionWorld : TkGoal term_id TkIs TkWillyIsAt term_num term_num
                        | TkGoal term_id TkIs term_num term_id TkObjectsInBasket
                        | TkGoal term_id TkIs term_num term_id TkObjectsAt term_num term_num'''
    global current_world, e

    if p[4] == "willy is at":
        # Define un nuevo objetivo en el mundo actual
        q = current_world.setGoalPosWilly(p[2], p[5], p[6])
        # Si ocurre un error asociado a este tipo de objetivo, se reporta
        if q != True:
            print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6]))
            if "dimensiones" in q:
                print("- Error en linea %s, columna %s: " % linenoLexpos(p, 5) + q)
            else:
                print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
            e = True

    elif p[6] == "objects in Basket":
        # Define un nuevo objetivo en el mundo actual
        q = current_world.setGoalObjBasket(p[2], p[4], p[5])
        # Si ocurre un error asociado a este tipo de objetivo, se reporta
        if q != True:
            print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6]))
            if "tipo objeto" in q:
                print("- Error en linea %s, columna %s: " % linenoLexpos(p, 5) + q)
            else:
                print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
            e = True

    elif p[6] == "objects at":
        # Define un nuevo objetivo en el mundo actual
        q = current_world.setGoalObjCelda(p[2], p[4], p[5], p[7], p[8])
        # Si ocurre un error asociado a este tipo de objetivo, se reporta
        if q != True:
            print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4])+" "+str(p[5])+" "+str(p[6])+" "+str(p[7])+" "+str(p[8]))
            if "tipo objeto" in q:
                print("- Error en linea %s, columna %s: " % linenoLexpos(p, 5) + q)
            elif "dimensiones" in q:
                print("- Error en linea %s, columna %s: " % linenoLexpos(p, 7) + q)
            else:
                print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
            e = True


# Instruccion de el Objetivo Final.
def p_instruccion_Final_goal(p):
    '''instruccionWorld : TkFinalGoalIs condicionGoal'''
    global current_world, e
    # Indica el objetivo final del mundo actual
    q = current_world.setFinalGoal(p[2])
    # Si ocurre un error asociado a este tipo de objetivo, se reporta y aborta
    if q != True:
        if "instruccion" in q:
            print("\n- Error en linea %s, columna %s: " % linenoLexpos(p, 1) + q)
        else:
            print("\n- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        e = True


# Define la condicion para que el programa sea exitoso.
def p_condicion_Goal(p):
    '''condicionGoal : condicionGoal TkAnd condicionGoal
                     | condicionGoal TkOr condicionGoal
                     | TkNot condicionGoal
                     | TkLParen condicionGoal TkRParen
                     | term_id'''

    if len(p) == 4:
        if (p[2] == "and") or (p[2] == "or"):
            p[0] = (p[2], p[1], p[3])

        elif (p[1] == "(") and (p[3] == ")"):
            p[0] = p[2]

    else:
        if p[1] == "not":
            p[0] = (p[1], p[2])

        else:
            p[0] = p[1]


################################################
#                     Task                     #
################################################

# Crea el nuevo task y lo agrega a la lista de tasks
def p_task(p):
    '''task : begintask instruccionesTask TkEndTask
            | begintask TkEndTask'''
    global current_task, list_of_tasks, TSimbolos

    # Si la tarea no es vacia, se le asigna su AST
    if len(p) == 4:
        current_task.setAST(p[2])
    # Agregamos la tarea a la lista de tareas totales
    list_of_tasks.append(current_task)
    current_task = None
    # Vaciamos la tabla de simbolos ya que terminamos el Task
    while not TSimbolos.empty():
        TSimbolos.pop()


# Inicializa un nuevo task. Esto se hace primero ya que necesitamos crear la instancia de Task
# para irla llenando mientras se realiza el parseo
def p_begintask(p):
    '''begintask : TkBeginTask term_id TkOn term_id'''
    global current_task, TSimbolos, bloq_num, e

    # Como no puede haber una tarea con el mismo identificador de un mundo
    # ni dos tareas con el mismo identificador. Se deben chequear los dos
    if checkExistingTaskId(p[2]):
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4]))
        print("- Error en linea %s, columna %s: No se puede utilizar un mismo identificador para definir dos tareas distintas." % linenoLexpos(p, 2))
        e = True
    if checkExistingWorldId(p[2]):
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4]))
        print("- Error en linea %s, columna %s: No se puede utilizar un mismo identificador para definir una tarea y un mundo." % linenoLexpos(p, 2))
        e = True
    # Chequea si la tarea esta siendo definida sobre un mundo que existe
    if not checkExistingWorldId(p[4]):
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4]))
        print("- Error en linea %s, columna %s: No se puede definir una tarea sobre un mundo no existente." % linenoLexpos(p, 4))
        e = True
    # Agregamos los simbolos del mundo donde opera el Task a la tabla de simbolos
    for i in range(len(list_of_world)):
        if list_of_world[i].getId() == p[4]:
            q = TSimbolos.insert(list_of_world[i])
            if q != True:
                print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3])+" "+str(p[4]))
                print("- Error en linea %s, columna %s: " % linenoLexpos(p, 4) + q)
                e = True
    # Se crea una instancia de Task y lo guardamos en current_task
    current_task = Task(p[2], p[4])
    # Aumentamos el numero de bloques del programa y le asignamos su numero
    # a el Task
    bloq_num += 1
    current_task.setBloqNum(bloq_num)


# Reduce las instrucciones
def p_instruccionesTask(p):
    '''instruccionesTask : instruccionesTask instruccionTask
                         | instruccionesTask TkSemiColon
                         | instruccionTask'''

    if (len(p) == 3) and (p[2] != ";"):
        instr = p[2]
        # No colocamos la instruccion "define" en el arbol del task
        if instr[0] == "define":
            p[0] = p[1]
        else:
            p[0] = (p[1], p[2])
    # Obviamos las ";" para las instrucciones que tienen mas de una de estas.
    elif (len(p) == 3) and (p[2] == ";"):
        p[0] = p[1]
    else:
        instr = p[1]
        # No colocamos la instruccion "define" en el arbol del task
        if instr[0] != "define":
            p[0] = p[1]
        else:
            p[0] = None


# Instruccion If, tambien cubre cuando es acompañado por el else
def p_instruccion_if(p):
    '''instruccionTask : TkIf test TkThen instruccionTask TkElse instruccionTask
                       | TkIf test TkThen instruccionTask'''

    if len(p) == 5:
        p[0] = (p[1], p[2], p[4])
    else:
        p[0] = (p[1], p[2], p[4], p[5], p[6])


# Instruccion repeat
def p_instruccion_repeat(p):
    '''instruccionTask : TkRepeat term_num TkTimes instruccionTask'''
    global e

    if p[2] <= 0:
        print("\n    "+str(p[1])+" "+str(p[2])+" "+str(p[3]))
        print("- Error en linea %s, columna %s: No se puede definir una iteracion acotada que repita un numero no positivo de veces." % linenoLexpos(p, 2))
        e = True
        
    p[0] = (p[1], p[2], p[4])


# Instruccion while
def p_instruccion_while(p):
    '''instruccionTask : TkWhile test TkDo instruccionTask'''

    p[0] = (p[1], p[2], p[4])


# Instruccion begin
def p_instruccion_begin(p):
    '''instruccionTask : TkBegin instruccionesTask TkEnd TkSemiColon'''

    p[0] = (p[1], p[2], p[3])

# Instruccion begin
def p_instruccion_begin_empty(p):
    '''instruccionTask : TkBegin TkEnd TkSemiColon'''

    p[0] = (p[1], None, p[2])


# Aqui detectamos cuando iniciamos una definicion de instruccion. Hacemos esto por separado
# ya que debemos guardar el num. de bloque de la instruccion a definir para evitar que
# una instruccion anidada tenga num. de bloque mayor que el de la instruccion externa
def p_define(p):
    '''define : TkDefine term_id'''
    global func_bloq_num, bloq_num

    # Aumentamos el numero de bloques total del programa
    bloq_num += 1
    # Agregamos el numero de bloque de la instruccion a definir en la pila
    # para que luego de definirse, podamos asignarle el numero
    func_bloq_num.append((p[2], bloq_num))

    p[0] = p[1]


# Instruccion que define una instruccion
def p_instruccion_define(p):
    '''instruccionTask : define TkAs instruccionTask'''
    global current_task, func_bloq_num, TSimbolos, list_of_instr, e

    # Obtenemos el num. de bloque y nombre de esta instruccion de la Tabla de simbolos
    name, FuncNum = func_bloq_num.pop()
    # Hacemos pop de la Tabla de simbolos a todas las instrucciones definidas dentro de esta instruccion.
    # Si no hacemos esto, podriamos llamar a una instruccion definida dentro de ella fuera de la instruccion compuesta.
    while FuncNum < TSimbolos.getTopBloqNum():
        TSimbolos.pop()
    # Obtenemos lo que haya en instruccionTask para revisar si es una
    # definicion de instruccion
    instr = p[3]
    # Si la instruccion es compuesta por otras instrucciones o es una que
    # define otra instruccion
    if len(instr) > 1:
        # Si es una definicion de instruccion, se agrega a la Tabla de simbolos pero no al AST de el Task
        if instr[0] == "define":
            p[0] = (p[1], name, None)
            # Si la instruccion no esta anidada, usamos el num. de bloque del Task como el bloque donde se encuentra la instruccion
            if len(func_bloq_num) == 0:
                f = Func(name, None, FuncNum, current_task.getBloqNum())
            # Si la instruccion es anidada, usamos el num. de bloque de la instruccion en donde se ecuentra
            else:
                f = Func(name, None, FuncNum, func_bloq_num[-1][1])
        else:
            p[0] = (p[1], name, p[3])
            # Si la instruccion no esta anidada, usamos el num. de bloque del Task como el bloque donde se encuentra la instruccion
            if len(func_bloq_num) == 0:
                f = Func(name, p[3], FuncNum, current_task.getBloqNum())
            # Si la instruccion es anidada, usamos el num. de bloque de la instruccion en donde se ecuentra
            else:
                f = Func(name, p[3], FuncNum, func_bloq_num[-1][1])
    # Si la instruccion no define otra instruccion
    else:
        p[0] = (p[1], name, p[3])
        # Si la instruccion no esta anidada, usamos el num. de bloque del Task como el bloque donde se encuentra la instruccion
        if len(func_bloq_num) == 0:
            f = Func(name, p[3], FuncNum, current_task.getBloqNum())
        # Si la instruccion es anidada, usamos el num. de bloque de la instruccion en donde se ecuentra
        else:
            f = Func(name, p[3], FuncNum, func_bloq_num[-1][1])
    # La insertamos en la tabla de simbolos
    q = TSimbolos.insert(f)
    if q != True:
        print("\n    "+str(p[1])+" "+str(name)+" "+str(p[2]))
        print("- Error en linea %s, columna %s: " % linenoLexpos(p, 2) + q)
        e = True
    # Agregamos la instruccion en la lista de instrucciones
    list_of_instr.append(f)
    

# Instruccion que llama una instruccion definida por el usuario
def p_instruccion_func(p):
    '''instruccionTask : term_id TkSemiColon'''
    global TSimbolos, e, func_bloq_num

    # Variable que indica si se encontro la instruccion que esta siendo referenciada 
    # en la tabla de simbolos o en la lista de instrucciones que se estan definiendo
    found = TSimbolos.find(p[1], "func")
    # Si lo encontramos en la tabla de simbolos, recuperamos el numero de bloque asociado a esta instruccion.
    if type(found) is not bool:
        bloq_num = found[1]
        found = True
        
    # Si no se encuentra en la tabla de simbolos, vemos si encontramos la llamada a 
    # la instruccion en la lista de instrucciones que estan siendo definidas, esto para permitir que se hagan llamadas recursivas
    i = len(func_bloq_num)-1
    while i >= 0 and not found:
        if func_bloq_num[i][0] == p[1]:
            found = True
            bloq_num = func_bloq_num[i][1]
        i -= 1
    # Si no encontramos la instruccion en la lista de instrucciones que se estan definiendo
    # ni en la tabla de simbolos, devolvemos un error
    if not found:
        print("\n    "+str(p[1]))
        print("- Error en linea %s, columna %s: '" % linenoLexpos(p, 1) + p[1] + "' no ha sido definido o no es una llamada a una instruccion.")
        bloq_num = None
        e = True

    p[0] = p[1] + " | " + str(bloq_num)

# Instruccion move
def p_instruccion_primitiva_move(p):
    '''instruccionTask : TkMove TkSemiColon'''

    p[0] = p[1]


# Instruccion turn-left
def p_instruccion_primitiva_turn_left(p):
    '''instruccionTask : TkTurnLeft TkSemiColon'''

    p[0] = p[1]


# Instruccion turn-right
def p_instruccion_primitiva_turn_right(p):
    '''instruccionTask : TkTurnRight TkSemiColon'''

    p[0] = p[1]


# Instruccion pick
def p_instruccion_primitiva_pick(p):
    '''instruccionTask : TkPick term_id TkSemiColon'''
    global TSimbolos, e

    if not TSimbolos.find(p[2], "objects"):
        print("\n    "+str(p[1])+" "+str(p[2]))
        print("- Error en linea %s, columna %s: '"  % linenoLexpos(p, 2) + p[2] + "' no ha sido definido o la variable no es un Objeto.")
        e = True

    p[0] = (p[1], p[2])
    

# Instruccion drop
def p_instruccion_primitiva_drop(p):
    '''instruccionTask : TkDrop term_id TkSemiColon'''
    global TSimbolos, e

    if not TSimbolos.find(p[2], "objects"):
        print("\n    "+str(p[1])+" "+str(p[2]))
        print("- Error en linea %s, columna %s: '"  % linenoLexpos(p, 2) + p[2] + "' no ha sido definido o la variable no es un Objeto.")
        e = True

    p[0] = (p[1], p[2])


# Instruccion set, cubre tambien cuando es acompañada por el to
def p_instruccion_primitiva_set(p):
    '''instruccionTask : TkSet term_id TkTo term_bool TkSemiColon
                       | TkSet term_id TkSemiColon'''
    global TSimbolos, e

    if not TSimbolos.find(p[2], "boolean"):
        print("\n    "+str(p[1])+" "+str(p[2]))
        print("- Error en linea %s, columna %s: '" % linenoLexpos(p, 2) + p[2] + "' no ha sido definido o la variable no es Booleana.")
        e = True

    if len(p) == 6:
        p[0] = (p[1], p[2], p[3], p[4])
    else:
        p[0] = (p[1], p[2])


# Instruccion clear
def p_instruccion_primitiva_clear(p):
    '''instruccionTask : TkClear term_id TkSemiColon'''
    global TSimbolos, e

    if not TSimbolos.find(p[2], "boolean"):
        print("\n    "+str(p[1])+" "+str(p[2]))
        print("- Error en linea %s, columna %s: '" % linenoLexpos(p, 2) + p[2] + "' no ha sido definido o la variable no es Booleana.")
        e = True

    p[0] = (p[1], p[2])


# Instruccion flip
def p_instruccion_primitiva_flip(p):
    '''instruccionTask : TkFlip term_id TkSemiColon'''
    global TSimbolos, e

    if not TSimbolos.find(p[2], "boolean"):
        print("\n    "+str(p[1])+" "+str(p[2]))
        print("- Error en linea %s, columna %s: '" % linenoLexpos(p, 2) + p[2] + "' no ha sido definido o la variable no es Booleana.")
        e = True

    p[0] = (p[1], p[2])


# Instruccion terminate
def p_instruccion_primitiva_terminate(p):
    '''instruccionTask : TkTerminate TkSemiColon'''

    p[0] = p[1]


# Define condiciones test en las tareas
def p_test(p):
    '''test : test TkAnd test
            | test TkOr test
            | TkNot test
            | term_bool
            | TkLParen test TkRParen
            | TkFrontClear
            | TkLeftClear
            | TkRightClear
            | TkLookingNorth
            | TkLookingEast
            | TkLookingSouth
            | TkLookingWest
            | TkFound TkLParen term_id TkRParen
            | TkCarrying TkLParen term_id TkRParen'''
    global TSimbolos, e

    if len(p) == 4:
        if (p[2] == "and") or (p[2] == "or"):
            p[0] = (p[2], p[1], p[3])

        elif (p[1] == "(") and (p[3] == ")"):
            p[0] = p[2]

    elif len(p) == 5:
        # Si el Id no es de tipo objeto o no esta definido en el mundo,
        # se devuelve un error.
        if not TSimbolos.find(p[3], "objects"):
            print("\n    "+str(p[1])+str(p[2])+str(p[3])+str(p[4]))
            print("- Error en linea %s, columna %s: '" % linenoLexpos(p, 3) + p[3] + "' no ha sido definido o la variable no es un Objeto.")
            e = True
        p[0] = (p[1], p[3])
    else:
        if p[1] == "not":
            p[0] = (p[1], p[2])

        else:
            p[0] = p[1]

# Define la condicion que usa un booleano definido en el mundo
def p_test_bool_world(p):
    '''test : term_id'''
    global TSimbolos, e

    if not TSimbolos.find(p[1], "boolean"):
        print("\n    "+str(p[1]))
        print("- Error en linea %s, columna %s: '" % linenoLexpos(p, 1) + p[1] + "' no ha sido definido o la variable no es Booleana.")
        e = True

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


# Regla para los errores de Sintaxis
def p_error(p):
    if p is not None:
        print("\n    " + str(p.value))
        print("- Error en la linea %s, columna %s" % (p.lineno, p.lexpos))
    sys.exit(0)
 
# Construye el parser
parser = yacc.yacc()