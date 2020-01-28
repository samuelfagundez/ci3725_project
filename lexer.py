# Proyecto CI3725 Primera entrega
# Pietro Iaia ID: 15-10718
# Pedro Samuel Fagundez ID: 15-10460

import sys
# Importamos el módulo lex de la librería PLY
# Esta librería es la que dará soporte para construir
# el interpretador durante el proyecto.
import ply.lex as lex
import string


# Definimos estados para diferenciar cuando estamos leyendo un bloque de comentario y cuando no
states = (
    ('CommentBlock', 'exclusive'),
)
# Variable que guarda la posicion del ultimo caracter \n encontrado, util para definir numero de columna
newline_pos = 0
# Variable booleana que indica si se encontraron errores durante la tokenizacion
e = False
# Variable que hace hace tracking al numero de comentarios abiertos
open_comments = 0

# Tokens que reconocerá el lexer basado en Willy*
tokens = [
    'TkId',
    'TkNum',
    'TkTrue',
    'TkFalse',
    'TkSemiColon',
    'TkPlus',
    'TkLParen',
    'TkRParen',
    'TkEquals',
    'TkStartCBlock',
    'TkEndCBlock',
    'TkBlockComment',
    'TkComment'
]

# Palabras reservadas que reconocerá el lexer
# basado en willy, al mismo tiempo las reconoce
# como tokens

reserved = {
    'begin-world': 'TkBeginWorld',
    'end-world': 'TkEndWorld',
    'World': 'TkWorld',
    'Wall': 'TkWall',
    'from': 'TkFrom',
    'to': 'TkTo',
    'north': 'TkNorth',
    'east': 'TkEast',
    'south': 'TkSouth',
    'west': 'TkWest',
    'Object-type': 'TkObjectType',
    'of color': 'TkOfColor',
    'red': 'TkRed',
    'blue': 'TkBlue',
    'magenta': 'TkMagenta',
    'cyan': 'TkCyan',
    'green': 'TkGreen',
    'yellow': 'TkYellow',
    'Place': 'TkPlace',
    'of': 'TkOf',
    'at': 'TkAt',
    'in basket ': 'TkInBasket',
    'Start at': 'TkStartAt',
    'heading': 'TkHeading',
    'Basket of capacity': 'TkBasketOfCapacity',
    'Boolean': 'TkBoolean',
    'with initial value': 'TkWithInitialValue',
    'Goal': 'TkGoal',
    'is': 'TkIs',
    'Final goal is': 'TkFinalGoalIs',
    'willy is at': 'TkWillyIsAt',
    'objects in Basket': 'TkObjectsInBasket',
    'objects at': 'TkObjectsAt',
    'and': 'TkAnd',
    'or': 'TkOr',
    'not': 'TkNot',
    'begin-work on': 'TkBeginWorkOn',
    'end-work': 'TkEndWork',
    'if': 'TkIf',
    'then': 'TkThen',
    'else': 'TkElse',
    'repeat': 'TkRepeat',
    'times': 'TkTimes',
    'while': 'TkWhile',
    'do': 'TkDo',
    'begin': 'TkBegin',
    'end': 'TkEnd',
    'define': 'TkDefine',
    'as': 'TkAs',
    'move': 'TkMove',
    'turn-left': 'TkTurnLeft',
    'turn-right': 'TkTurnRight',
    'pick': 'TkPick',
    'drop': 'TkDrop',
    'set': 'TkSet',
    'clear': 'TkClear',
    'flip': 'TkFlip',
    'terminate': 'TkTerminate',
    'front-clear': 'TkFrontClear',
    'left-clear': 'TkLeftClear',
    'right-clear': 'TkRightClear',
    'looking-north': 'TkLookingNorth',
    'looking-east': 'TkLookingEast',
    'looking-south': 'TkLookingSouth',
    'looking-west': 'TkLookingWest',
    'found': 'TkFound',
    'carrying': 'TkCarrying'
}

# La lista de tokens entonces será los tokens predefinidos
# unidos a las palabras reservadas
tokens = tokens + list(reserved.values())

# Los token definidos por string son ordenados por el largo de su regex y agregados en orden decreciente
t_ignore = ' \t'                       # Ignora los espacios en blanco y tab
t_CommentBlock_ignore = ' \t'          # Ignora los espacios en blanco y tab


# Si encontramos un punto y coma (;) retornamos el token

def t_TkSemiColon(t):
    r'\;'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos un signo de suma (+) retornamos el token

def t_TkPlus(t):
    r'\+'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos un parentesis abierto [(] retornamos el token

def t_TkLParen(t):
    r'\('
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos un signo igual (=) retornamos el token

def t_TkEquals(t):
    r'\='
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos un parentesis cerrado [)] retornamos el token

def t_TkRParen(t):
    r'\)'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si leemos un '{{' entramos al estado de Bloque de comentario

def t_TkStartCBlock(t):
    r'\{{'
    global open_comments
    open_comments += 1
    t.lexer.begin('CommentBlock')
    pass


# Si leemos un '}}' entramos al estado inicial

def t_CommentBlock_TkEndCBlock(t):
    r'\}}'
    global open_comments
    open_comments -= 1
    if(open_comments == 0): t.lexer.begin('INITIAL')
    pass


# Si encontramos un bloque de comentario dentro del bloque de comentario, devolvemos un error

def t_CommentBlock_TkBlockComment(t):
    r'{{[^\}]*}}'
    global e
    global open_comments
    # Si se detecta un error, e = True
    e = True
    open_comments += t.value.count('{{') - t.value.count('}}')
    # Define el numero de columna en el que se encuentra el token
    t.lexpos = (t.lexpos - newline_pos) + 1
    print("Error: Comentario anidado en " + str(t.lineno) + ", " + str(t.lexpos))
    t.lexer.lineno += t.value.count('\n') 
    pass


# Si encontramos -- significa que ignoramos de allí en adelante
# incluidos los --
def t_TkComment(t):
    r'\--.*'
    pass


# Si encontramos la palabra TRUE retornamos el token

def t_TkTrue(t):
    r'true'
    t.value = True
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra FALSE retornamos el token

def t_TkFalse(t):
    r'false'
    t.value = False
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra <of color> retornamos el token

def t_TkOfColor(t):
    r'of[ ]color'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t

# Si encontramos la palabra <begin-work on> retornamos el token

def t_TkBeginWorkOn(t):
    r'begin-work[ ]on'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra <in basket> retornamos el token

def t_TkInBasket(t):
    r'in[ ]basket'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra <Start at> retornamos el token

def t_TkStartAt(t):
    r'Start[ ]at'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra <Basket of capacity> retornamos el token

def t_TkBasketOfCapacity(t):
    r'Basket[ ]of[ ]capacity'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra <with initial value> retornamos el token

def t_TkWithInitialValue(t):
    r'with[ ]initial[ ]value'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra <Final goal is> retornamos el token

def t_TkFinalGoalIs(t):
    r'Final[ ]goal[ ]is'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra <willy is at> retornamos el token

def t_TkWillyIsAt(t):
    r'willy[ ]is[ ]at'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra <objects in basket> retornamos el token

def t_TkObjectsInBasket(t):
    r'objects[ ]in[ ]Basket'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos la palabra <objects at> retornamos el token

def t_TkObjectsAt(t):
    r'objects[ ]at'
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Si encontramos cualquier sting que cumpla el siguiente formato
# y que no sea ninguna de las palabras reservadas anteriores
# entonces retornamos el token

def t_TkId(t):
    r'[a-zA-Z_][a-zA-Z_0-9\-]*'
    t.type = reserved.get(t.value, 'TkId')
    t.lexpos = (t.lexpos - newline_pos) + 1
    if (t.value.count('-') >= 1 and t.type == 'TkId'):
        # Si se detecta un error, e = True
        global e
        e = True
        # Posicion del ultimo '-' encontrado en el Id
        pos = 0
        # Mostramos todos estos errores
        for i in range(0, t.value.count('-')):
            pos = t.value.find('-', pos+1)
            print("Caracter ilegal '-' encontrado en la linea %i, columna %i" % (t.lineno, t.lexpos + pos))
    else:
        return t


# Si encontramos un entero retornamos el token

def t_TkNum(t):
    r'\d+'
    t.value = int(t.value)
    t.lexpos = (t.lexpos - newline_pos) + 1
    return t


# Saltos de linea

def t_ANY_newline(t):
    r'\n'
    # Actualiza la variable global con la posicion del ultimo \n encontrado
    global newline_pos
    newline_pos = t.lexpos + 1     
    t.lexer.lineno += len(t.value)


# Muestra el error, gracias a la liberería PLY, ya imprime
# todos los caracteres ilegales

def t_error(t):
    # Si se detecta un error, e = True
    global e
    e = True
    t.lexpos = (t.lexpos - newline_pos) + 1
    print("Caracter ilegal '%s' encontrado en la linea %i, columna %i" %
          (t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)


# Muestra el error

def t_CommentBlock_error(t):
    t.lexer.skip(1)


# Funcion usada por files.py para checkear si se encontraron errores durante la tokenizacion

def checkError():
    return e


# Construye el Lexer
lexer = lex.lex()