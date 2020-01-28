import sys
from os import listdir, getcwd
from lexer import lexer, checkError

# ruta actual + /pruebas

# funcion que recibe una ruta y devuelve una lista de
# todos los archivos en ese directorio, si no es directorio falla

# funcion que se encarga de abrir un archivo enviarlo al lexer e imprimir el resultado


def readFile(path):
    # obtener el directorio actual y concatenar con la direccion del archivo a abrir.
    rutaGlobal = getcwd()+"/"+path
    # apertura del archivo
    fp = open(rutaGlobal, "r")
    # el contenido del archivo se lo pasamos al lexer
    content = fp.read()
    lexer.input(content)
    # variable auxiliar que nos servirá para saber en que linea del archivo nos encontramos
    i = 0
    # Estructura de tipo listas de listas donde cada elemento de la lista es otro lista
    # Por ejemplo la posicion 0 de la lista contiene los tokens de la primera linea,
    # la posicion n-1 de la lista contiene los tokens de la linea n.
    list = [[]]
    # procesamiento de todos los tokens
    while True:
        # tomamos cada token que devuelve el lexer
        tok = lexer.token()
        # si se acabaron los tokens o ya terminamos de leer break
        if not tok:
            break
        # leo los tokens de una linea
        if tok.lineno == i+1:
            list[i].append(tok)
        # si el token ya saltó de linea...
        elif tok.lineno > i+1:
            # buscamos la linea donde vuelva a tener tokens
            while(tok.lineno > i+1):
                # colocamos un elemento de lista vacío por cada linea vacia
                list.append([])
                # iteramos
                i += 1
            # una vez encontramos token lo añadimos en la ultima posicion
            list[i].append(tok)
    # Si no se encontraron errores, se imprimen los Tokens
    if(not checkError()):
        # para cada elemento en la lista que representan cada linea...
        for listItem in list:
            # variable spaces que usaremos para la identación
            spaces = 0
            # si el tamaño del elemento de la lista es 0 es porque es una linea vacía.
            if len(listItem) == 0:
                print("")
            # si no es 0
            else:
                # para dentro de las listas de la lista hay tokens si su length es distinto de 0
                for token in listItem:
                    # añadimos tantos espacios como hayan entre 0 y el numero de la columna, y solo lo hacemos para el primer token de cada linea
                    while(spaces != token.lexpos-1 and listItem.index(token) == 0):
                        print("", end=" ")
                        spaces += 1
                    # si el token es de tipo num imprimimos con este formato
                    if token.type == 'TkNum':
                        print("%s(valor=%i, linea=%i, columna=%i)" % (
                            token.type, token.value, token.lineno, token.lexpos), end=" ")
                    # si el token es de tipo id imprimimos con este formato
                    elif token.type == 'TkId':
                        print('%s(valor="%s", linea=%i, columna=%i)' % (token.type,
                                                                        token.value, token.lineno, token.lexpos), end=" ")
                    # si el token es de otro tipo imprimimos con este formato
                    else:
                        print("%s(linea=%i, columna=%i)" %
                              (token.type, token.lineno, token.lexpos), end=" ")
            # salto de linea entre tokens
            if len(listItem) != 0:
                print("")
    fp.close()
