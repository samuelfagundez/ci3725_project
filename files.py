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
    # procesamiento
    content = fp.read()
    lexer.input(content)
    i = 0
    # almacenamiento de tokens en la lista.
    list = [[]]
    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.lineno == i+1:
            list[i].append(tok)
        elif tok.lineno > i+1:
            while(tok.lineno > i+1):
                list.append([])
                i += 1
            list[i].append(tok)
    # Si no se encontraron errores, se imprimen los Tokens
    if(not checkError()):
        for listItem in list:
            if len(listItem) == 0:
                print("")
            else:
                for token in listItem:
                    if token.type == 'TkNum':
                        print("%s(%i, linea=%i, columna=%i)" % (
                            token.type, token.value, token.lineno, token.lexpos), end=" ")
                    elif token.type == 'TkId':
                        print('%s("%s", linea=%i, columna=%i)' % (token.type,
                                                                  token.value, token.lineno, token.lexpos), end=" ")
                    else:
                        print("%s(linea=%i, columna=%i)" %
                              (token.type, token.lineno, token.lexpos), end=" ")
            if len(listItem) != 0:
                print("")
    fp.close()
