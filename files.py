import sys
from os import listdir, getcwd
from samlexer import lexer

# rutaGlobal = '/home/samuel/Documents/ci3725_project/pruebas'
rutaGlobal = getcwd()+'/pruebas'


def ls(ruta):
    return listdir(ruta)


archivos = ls(rutaGlobal)


def readFile(path):
    fp = open(ruta, "r")
    content = fp.read()
    lexer.input(content)
    fp.close()


for archivo in archivos:
    ruta = rutaGlobal+"/"+archivo
    readFile(ruta)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
