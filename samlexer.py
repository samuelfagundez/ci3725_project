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
    'EQUALS'
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
    'in basket': 'INBASKET',
    'basket of capacity': 'BASKETOFCAPACITY',
    'with initial value': 'WITHINITIALVALUE',
    'final goal': 'FINALGOAL',
    'heading': 'HEADING',
    'boolean': 'BOOLEAN',
    'goal': 'GOAL',
    'is': 'IS',
    'not': 'NOT'
}

tokens = tokens+list(reserved.values())

print(tokens)

t_SEMICOLON = r'\;'
t_LPAREN = r'\('
t_EQUALS = r'\='
t_RPAREN = r'\)'


def t_COMMENT(t):
    r'\--.*'
    pass


def t_BLOCKCOMMENT(t):
    r'\{{.*}}'
    pass


def t_INBASKET(t):
    r'in[ ]basket'
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
