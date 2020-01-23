# Proyecto CI3725 Primera entrega
# Pietro Iaia ID: 15-10718
# Pedro Samuel Fagundez ID: 15-10460

import sys
# Importamos el módulo lex de la librería PLY
# Esta librería es la que dará soporte para construir
# el interpretador durante el proyecto.
import ply.lex as lex


# Definimos estados para diferenciar cuando estamos leyendo un bloque de comentario y cuando no
states = (
    ('CommentBlock', 'exclusive'),
)
# Variable que guarda la posicion del ultimo caracter \n encontrado, util para definir numero de columna
newline_pos = 0

# Tokens que reconocerá el lexer basado en Willy*
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

# Palabras reservadas que reconocerá el lexer
# basado en willy, al mismo tiempo las reconoce
# como tokens

reserved = {
    'begin-world': 'BEGIN_WORLD',
    'end-world': 'END_WORLD',
    'World': 'WORLD',
    'Wall': 'WALL',
    'from': 'FROM',
    'to': 'TO',
    'north': 'NORTH',
    'east': 'EAST',
    'south': 'SOUTH',
    'west': 'WEST',
    'Object-type': 'OBJECT_TYPE',
    'of color': 'OF_COLOR',
    'red': 'RED',
    'blue': 'BLUE',
    'magenta': 'MAGENTA',
    'cyan': 'CYAN',
    'green': 'GREEN',
    'yellow': 'YELLOW',
    'Place': 'PLACE',
    'of': 'OF',
    'at': 'AT',
    'in basket ': 'IN_BASKET',
    'Start at': 'START_AT',
    'heading': 'HEADING',
    'Basket of capacity': 'BASKET_OF_CAPACITY',
    'Bolean': 'BOOLEAN',
    'with initial value': 'WITH_INITIAL_VALUE',
    'Goal': 'GOAL',
    'is': 'IS',
    'Final goal is': 'FINAL_GOAL_IS',
    'willy is at': 'WILLY_IS_AT',
    'objects in Basket': 'OBJECTS_IN_BASKET',
    'objects at': 'OBJECTS_AT',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'begin-work': 'BEGIN_WORK',
    'end-work': 'END_WORK',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'repeat': 'REPEAT',
    'times': 'TIMES',
    'while': 'WHILE',
    'do': 'DO',
    'begin': 'BEGIN',
    'end': 'END',
    'define': 'DEFINE',
    'as': 'AS',
    'move': 'MOVE',
    'turn-left': 'TURN_LEFT',
    'turn-right': 'TURN_RIGHT',
    'pick': 'PICK',
    'drop': 'DROP',
    'set': 'SET',
    'clear': 'CLEAR',
    'flip': 'FLIP',
    'terminate': 'TERMINATE',
    'front-clear': 'FRONT_CLEAR',
    'left-clear': 'LEFT_CLEAR',
    'right-clear': 'RIGHT_CLEAR',
    'looking-north': 'LOOKING_NORTH',
    'looking-east': 'LOOKING_EAST',
    'looking-south': 'LOOKING_SOUTH',
    'looking-west': 'LOOKING_WEST',
    'found': 'FOUND',
    'carrying': 'CARRYING'
}

# La lista de tokens entonces será los tokens predefinidos
# unidos a las palabras reservadas
tokens = tokens + list(reserved.values())


t_SEMICOLON = r'\;'
# Los token definidos por string son ordenados por el largo de su regex y agregados en orden decreciente
t_PLUS = r'\+'
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
    # Define el numero de columna en el que se encuentra el token
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos -- significa que ignoramos de allí en adelante
# incluidos los --
def t_COMMENT(t):
    r'\--.*'
    pass

# Si encontramos la palabra TRUE retornamos el token


def t_TRUE(t):
    r'true'
    t.value = True
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra FALSE retornamos el token

def t_FALSE(t):
    r'false'
    t.value = False
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Como tener tokens con espacios, NOTA: Tiene que estar definido primero que t_ID

# Si encontramos la palabra <of color> retornamos el token


def t_OF_COLOR(t):
    r'of[ ]color'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos la palabra <in basket> retornamos el token


def t_IN_BASKET(t):
    r'in[ ]basket'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos la palabra <Start at> retornamos el token


def t_START_AT(t):
    r'Start[ ]at'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos la palabra <Basket of capacity> retornamos el token


def t_BASKET_OF_CAPACITY(t):
    r'Basket[ ]of[ ]capacity'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos la palabra <with initial value> retornamos el token


def t_WITH_INITIAL_VALUE(t):
    r'with[ ]initial[ ]value'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos la palabra <Final goal is> retornamos el token


def t_FINAL_GOAL_IS(t):
    r'Final[ ]goal[ ]is'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos la palabra <willy is at> retornamos el token


def t_WILLY_IS_AT(t):
    r'willy[ ]is[ ]at'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos la palabra <objects in basket> retornamos el token


def t_OBJECTS_IN_BASKET(t):
    r'objects[ ]in[ ]basket'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos la palabra <objects at> retornamos el token


def t_OBJECTS_AT(t):
    r'objects[ ]at'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos cualquier sting que cumpla el siguiente formato
# y que no sea ninguna de las palabras reservadas anteriores
# entonces retornamos el token


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value, 'ID')
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos un entero retornamos el token


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Saltos de linea


def t_newline(t):
    r'\n+'
    # Actualiza la variable global con la posicion del ultimo \n encontrado
    global newline_pos
    newline_pos = t.lexpos                                  #
    t.lexer.lineno += len(t.value)

# Muestra el error, gracias a la liberería PLY, ya imprime
# todos los caracteres ilegales


def t_error(t):
    t.lexpos = (t.lexpos - newline_pos) + 1
    print("Caracter ilegal '%s' encontrado en la linea %i, columna %i" %
          (t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)

# Muestra el error


def t_CommentBlock_error(t):
    t.lexer.skip(1)


# Construye el Lexer
lexer = lex.lex()
