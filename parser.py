import ply.yacc as yacc
from lexer import tokens
from World import World


list_of_world = []
current_world = None 
# Son ordenados de menor a mayor precedencia
precedence = (
    ('left', 'TkAnd'),
    ('left', 'TkOr'),
    ('right', 'TkNot')
)

# la regla gramatica inicial es la funcion mas arriba en el archivo, aqui es donde el parser debe llegar y 
# una vez que llega se detiene y regresa el valor en p[0]. Si el parser no llega aqui, se da un syntax error.

def p_world(p):
    '''world : beginworld instrucciones TkEndWorld'''
    ##########################################
    print(current_world.worldDim())
    print(current_world.walls)
    print(current_world.objetivos)
    print(current_world.getFinalGoal())
    print(current_world.objects)
    print(current_world.basketCapacity)
    print(current_world.willyBasket)
    print(current_world.willyPos)
    print(current_world.booleanos)
    ##########################################

def p_beginworld(p):
    '''beginworld : TkBeginWorld term_id'''
    global current_world
    current_world = World(p[2])

def p_instrucciones(p):
    '''instrucciones : instrucciones TkSemiColon instruccion
                     | instruccion'''

# Intruccion World
def p_instruccion_World(p):
    '''instruccion : TkWorld term_num term_num'''
    global current_world
    current_world.newWorld(p[2], p[3])

# Intruccion Wall
def p_instruccion_Wall(p):
    '''instruccion : TkWall term_dir TkFrom term_num term_num TkTo term_num term_num'''
    global current_world
    current_world.newWall(p[2], p[4], p[5], p[7], p[8])

# Intruccion Object-type
def p_instruccion_Object_type(p):
    '''instruccion : TkObjectType term_id TkOfColor term_color'''
    global current_world
    current_world.newObject(p[2], p[4])

# Intruccion Place en casilla
def p_instruccion_Place_casilla(p):
    '''instruccion : TkPlace term_num TkOf term_id TkAt term_num term_num'''
    global current_world
    current_world.placeInWorld(p[2], p[4], p[6], p[7])

# Intruccion Place en bolsa
def p_instruccion_Place_in_basket(p):
    '''instruccion : TkPlace term_num TkOf term_id TkInBasket'''
    global current_world
    current_world.placeInBasket(p[2], p[4])

# Intruccion Start de willy
def p_instruccion_Start_willy(p):
    '''instruccion : TkStartAt term_num term_num TkHeading term_dir'''
    global current_world
    current_world.willyStartAt(p[2], p[3], p[5])

# Intruccion Basket of capacity
def p_instruccion_Basket_capacity(p):
    '''instruccion : TkBasketOfCapacity term_num'''
    global current_world
    current_world.setCapacityOfBasket(p[2])

# Intruccion que define Booleano
def p_instruccion_Boolean(p):
    '''instruccion : TkBoolean term_id TkWithInitialValue term_bool'''
    global current_world
    current_world.newBoolean(p[2], p[4])

# Intruccion Goal
def p_instruccion_Goal(p):
    '''instruccion : TkGoal term_id TkIs TkWillyIsAt term_num term_num
                   | TkGoal term_id TkIs term_num term_id TkObjectsInBasket
                   | TkGoal term_id TkIs term_num term_id TkObjectsAt term_num term_num'''
    global current_world
    if p[4] == "willy is at":
        current_world.setGoalPosWilly(p[2], p[5], p[6])
    elif p[6] == "objects in Basket":
        current_world.setGoalObjBasket(p[2], p[4], p[5])
    elif p[6] == "objects at":
        current_world.setGoalObjCelda(p[2], p[4], p[5], p[7], p[8])

# Instruccion de el Objetivo Final. Esto puede cambiar, creo que no se hace asi !!!!!!!!
def p_instruccion_Final_goal(p):
    '''instruccion : TkFinalGoalIs condicionGoal'''
    global current_world
    current_world.setFinalGoal(p[2])

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


# Terminal numero {0,1,...,9}
def p_term_num(p):
    '''term_num : TkNum'''
    p[0] = p[1]

# Terminal Booleano {true, false}
def p_term_bool(p):
    '''term_bool : TkTrue
                 | TkFalse'''

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


#def p_test_and(p):
#    '''test : test TkAnd term_bool '''
#    p[0] = p[1] and p[3]

#def p_test_or(p):
#    '''test : test TkOr term_bool '''
#    p[0] = p[1] or p[3]

#def p_test_not(p):
#    '''test : TkNot test'''
#    p[0] = not p[2]

#def p_test_term_bool(p):
#    '''test : term_bool'''
#    p[0] = p[1]


# Regla para los errores de Sintaxis
def p_error(p):
    print("Syntax error in input!")
 
# Construye el parser
parser = yacc.yacc()
 

try:
    fp = open("prueba.txt", "r")
    s = fp.read()
except EOFError:
    pass
result = parser.parse(s)
print(result)
