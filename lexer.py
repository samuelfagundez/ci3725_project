import ply.lex as lex
import sys

# Todo esto esta en la pagina de documentacion de PLY: https://www.dabeaz.com/ply/ply.html#ply_nn14b


tokens = [
    'ID',
    'INT',
    'FLOAT',
    'SEMICOLON',
    'PLUS',
    'MULTIPLY',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EQUALS'
]

reserved = {
    'begin-world' : 'BEGIN_WORLD',
    'end-world' : 'END_WORLD',
    'and' : 'AND',
    'or' : 'OR',
    'World' : 'WORLD',
    'Wall' : 'WALL',
    'from' : 'FROM',
    'to' : 'TO',
    'Object-type' : 'OBJECT_TYPE',
    'Place' : 'PLACE',
    'in basket' : 'IN_BASKET',
    'of' : 'OF',
    'at' : 'AT',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'repeat' : 'REPEAT',
    'times' : 'TIMES',
    'begin' : 'BEGIN',
    'end' : 'END',
    'define' : 'DEFINE',
    'as' : 'AS'
}

tokens = tokens + list(reserved.values())

t_SEMICOLON = r'\;'
t_PLUS = r'\+'                         # Los token definidos por string son ordenados por el largo de su regex y agregados en orden decreciente
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_EQUALS = r'\='
t_RPAREN = r'\)'


# Como tener tokens con espacios, NOTA: Tiene que estar definido primero que t_ID
def t_IN_BASKET(t):
    r'in[ ]basket'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_FLOAT(t):                         # FLOAT va primero que INT ya que los tokens definido con funciones son agregados en el orden en el que aparecen
    r'\d+\.\d+'
    t.value = float(t.value)
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