import ply.lex as lex
import ply.yacc as yacc

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
    'MINUS'
]

reserved = {
    'begin-world': 'BEGIN_WORLD',
    'end-world': 'END_WORLD',
    'and': 'AND',
    'or': 'OR',
    'World': 'WORLD',
    'Wall': 'WALL',
    'from': 'FROM',
    'to': 'TO',
    'Object-type': 'OBJECT_TYPE',
    'Place': 'PLACE',
    'of': 'OF',
    'at': 'AT',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'repeat': 'REPEAT',
    'times': 'TIMES',
    'begin': 'BEGIN',
    'end': 'END',
    'define': 'DEFINE',
    'as': 'AS',
    #
    'in basket': 'IN_BASKET',
    'basket of capacity': 'BASKET_OF_CAPACITY',
    'with initial value': 'WITH_INITIAL_VALUE',
    'final goal': 'FINAL_GOAL',
    'heading': 'HEADING',
    'boolean': 'BOOLEAN',
    'goal': 'GOAL',
    'is': 'IS',
    'not': 'NOT'
}

tokens = tokens+list(reserved.values())

t_SEMICOLON = r'\;'
t_LPAREN = r'\('
t_EQUALS = r'\='
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'


def t_COMMENT(t):
    r'\--.*'
    pass


def t_BLOCKCOMMENT(t):
    r'\{{.*}}'
    pass


def t_IN_BASKET(t):
    r'in[ ]basket'
    t.type = reserved.get(t.value, 'IN_BASKET')
    return t


def t_BASKET_OF_CAPACITY(t):
    r'[Bb]asket[ ]of[ ]capacity'
    t.type = reserved.get(t.value, 'BASKET_OF_CAPACITY')
    return t


def t_WITH_INITIAL_VALUE(t):
    r'with[ ]initial[ ]value'
    t.type = reserved.get(t.value, 'WITH_INITIAL_VALUE')
    return t


def t_FINAL_GOAL(t):
    r'final[ ]goal'
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
#     tok = analizador.token()
#     if not tok:
#         break
#     print(tok)
