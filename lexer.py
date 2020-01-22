import ply.lex as lex
import sys


# Definimos estados para diferenciar cuando estamos leyendo un bloque de comentario y cuando no
states = (
    ('CommentBlock', 'exclusive'),
    )
# Variable que guarda la posicion del ultimo caracter \n encontrado, util para definir numero de columna
newline_pos = 0

tokens = [
    'ID',
    'INT',
    'TRUE',
    'FALSE',
    'SEMICOLON',
    'PLUS',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'START_CBLOCK',
    'END_CBLOCK',
    'BLOCKCOMMENT',
]

reserved = {
    'begin-world' : 'BEGIN_WORLD',
    'end-world' : 'END_WORLD',
    'World' : 'WORLD',
    'Wall' : 'WALL',
    'from' : 'FROM',
    'to' : 'TO',
    'north' : 'NORTH',
    'east' : 'EAST',
    'south' : 'SOUTH',
    'west' : 'WEST',
    'Object-type' : 'OBJECT_TYPE',
    'of color' : 'OF_COLOR',
    'red' : 'RED',
    'blue' : 'BLUE',
    'magenta' : 'MAGENTA',
    'cyan' : 'CYAN',
    'green' : 'GREEN',
    'yellow' : 'YELLOW',
    'Place' : 'PLACE',
    'of' : 'OF',
    'at' : 'AT',
    'in basket ' : 'IN_BASKET',
    'Start at' : 'START_AT',
    'heading' : 'HEADING',
    'Basket of capacity' : 'BASKET_OF_CAPACITY',
    'Bolean' : 'BOOLEAN',
    'with initial value' : 'WITH_INITIAL_VALUE',
    'Goal' : 'GOAL',
    'is' : 'IS',
    'Final goal is' : 'FINAL_GOAL_IS',
    'willy is at' : 'WILLY_IS_AT',
    'objects in Basket' : 'OBJECTS_IN_BASKET',
    'objects at' : 'OBJECTS_AT',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'begin-work' : 'BEGIN_WORK',
    'end-work' : 'END_WORK',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'repeat' : 'REPEAT',
    'times' : 'TIMES',
    'while' : 'WHILE',
    'do' : 'DO',
    'begin' : 'BEGIN',
    'end' : 'END',
    'define' : 'DEFINE',
    'as' : 'AS',
    'move' : 'MOVE',
    'turn-left' : 'TURN_LEFT',
    'turn-right' : 'TURN_RIGHT',
    'pick' : 'PICK',
    'drop' : 'DROP',
    'set' : 'SET',
    'clear' : 'CLEAR',
    'flip' : 'FLIP',
    'terminate' : 'TERMINATE',
    'front-clear' : 'FRONT_CLEAR',
    'left-clear' : 'LEFT_CLEAR',
    'right-clear' : 'RIGHT_CLEAR',
    'looking-north' : 'LOOKING_NORTH',
    'looking-east' : 'LOOKING_EAST',
    'looking-south' : 'LOOKING_SOUTH',
    'looking-west' : 'LOOKING_WEST',
    'found' : 'FOUND',
    'carrying' : 'CARRYING'
}

tokens = tokens + list(reserved.values())


t_SEMICOLON = r'\;'
t_PLUS = r'\+'                         # Los token definidos por string son ordenados por el largo de su regex y agregados en orden decreciente
t_LPAREN = r'\('
t_EQUALS = r'\='
t_RPAREN = r'\)'
t_ignore = ' \t'                       # Ignora los espacios en blanco y tab
t_CommentBlock_ignore = ' \t'          # Ignora los espacios en blanco y tab


# Si leemos un '{{' entramos al estado de Bloque de comentario
def t_START_CBLOCK(t):
    r'\{{'
    t.lexer.begin('CommentBlock')
    pass

# Si leemos un '}}' entramos al estado inicial
def t_CommentBlock_END_CBLOCK(t):
    r'\}}'
    t.lexer.begin('INITIAL')
    pass

# Si encontramos un bloque de comentario dentro del bloque de comentario, devolvemos un error
def t_CommentBlock_BLOCKCOMMENT(t):
    r'\{{(.*\n*)*}}'
    t.lexpos = (t.lexpos - newline_pos) + 1          # Define el numero de columna en el que se encuentra el token
    return t

def t_COMMENT(t):
    r'\--.*'
    pass

def t_TRUE(t):
    r'true'
    t.value = True
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Como tener tokens con espacios, NOTA: Tiene que estar definido primero que t_ID
def t_OF_COLOR(t):
    r'of[ ]color'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_IN_BASKET(t):
    r'in[ ]basket'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_START_AT(t):
    r'Start[ ]at'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_BASKET_OF_CAPACITY(t):
    r'Basket[ ]of[ ]capacity'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_WITH_INITIAL_VALUE(t):
    r'with[ ]initial[ ]value'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_FINAL_GOAL_IS(t):
    r'Final[ ]goal[ ]is'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_WILLY_IS_AT(t):
    r'willy[ ]is[ ]at'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_OBJECTS_IN_BASKET(t):
    r'objects[ ]in[ ]basket'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_OBJECTS_AT(t):
    r'objects[ ]at'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value, 'ID')
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)   
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

def t_newline(t):
    r'\n+'
    global newline_pos                                      # Actualiza la variable global con la posicion del ultimo \n encontrado
    newline_pos = t.lexpos                                  #
    t.lexer.lineno += len(t.value)

# Muestra el error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Muestra el error
def t_CommentBlock_error(t):
    t.lexer.skip(1)


# Construye el Lexer
lexer = lex.lex()