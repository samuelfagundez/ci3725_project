import ply.lex as lex

import sys


tokens = [
    'ID',  # identificador como el nombre de un mundo
    'INT',  # enteros como las columnas o filas
    'SEMICOLON',  # separador
    'TRUE',
    'FALSE',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'PLUS',
]

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
    'while': 'WHILE',
    'repeat': 'REPEAT',
    'times': 'TIMES',
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

tokens = tokens+list(reserved.values())

t_SEMICOLON = r'\;'
t_LPAREN = r'\('
t_EQUALS = r'\='
t_RPAREN = r'\)'
t_PLUS = r'\+'


def t_COMMENT(t):
    r'\--.*'
    pass


def t_BLOCKCOMMENT(t):
    r'\{{.*}}'
    pass


def t_TRUE(t):
    r'true'
    t.value = True
    return t


def t_FALSE(t):
    r'false'
    t.value = False
    return t


def t_OF_COLOR(t):
    r'of[ ]color'
    return t


def t_IN_BASKET(t):
    r'in[ ]basket'
    return t


def t_STAR_AT(t):
    r'Start[ ]at'
    return t


def t_BASKET_OF_CAPACITY(t):
    r'Basket[ ]of[ ]capacity'
    return t


def t_WITH_INITIAL_VALUE(t):
    r'with[ ]initial[ ]value'
    return t


def t_FINAL_GOAL_IS(t):
    r'Final[ ]goal[ ]is'
    return t


def t_WILLY_IS_AT(t):
    r'willy[ ]is[ ]at'
    return t


def t_OBJECTS_IN_BASKET(t):
    r'objects[ ]in[ ]basket'
    return t


def t_OBJECTS_AT(t):
    r'objects[ ]at'
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Ignora los espacios en blanco
t_ignore = ' \t'

# Muestra el error


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Construye el Lexer
lexer = lex.lex()

# lexer.input("begin-world Place 5 of web in basket end-world")

# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
