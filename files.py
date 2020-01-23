import sys
from os import listdir, getcwd
from lexer import lexer

# ruta actual + /pruebas
rutaGlobal = getcwd()+'/pruebas'

# funcion que recibe una ruta y devuelve una lista de
# todos los archivos en ese directorio, si no es directorio falla


def ls(ruta):
    return listdir(ruta)


archivos = ls(rutaGlobal)

# funcion que se encarga de abrir un archivo enviarlo al lexer e imprimir el resultado


def readFile(path):
    fp = open(ruta, "r")
    content = fp.read()
    lexer.input(content)
    i = 0
    list = [[]]
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.lexer.lineno == i+1:
            list[i].append(tok)
        elif tok.lexer.lineno == i+2:
            list.append([])
            i = i + 1
            list[i].append(tok)
        else:
            list.append([])
            i = i + 1
    for listItem in list:
        if len(listItem) == 0:
            print("")
        else:
            for token in listItem:
                if token.type == 'INT':
                    print("%s(%i, linea=%i, columna=%i)" % (
                        token.type, token.value, token.lineno, token.lexpos), end=" ")
                elif token.type == 'ID':
                    print('%s("%s", linea=%i, columna=%i)' % (token.type,
                                                              token.value, token.lineno, token.lexpos), end=" ")
                else:
                    print("%s(linea=%i, columna=%i)" %
                          (token.type, token.lineno, token.lexpos), end=" ")
        if len(listItem) != 0:
            print("")
    fp.close()


# funcion q se encarga de llamar a readFile con cada archivo de una ruta
for archivo in archivos:
    ruta = rutaGlobal+"/"+archivo
    readFile(ruta)
