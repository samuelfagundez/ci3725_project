import sys
from os import listdir, getcwd
from samlexer import lexer

# rutaGlobal = '/home/samuel/Documents/ci3725_project/pruebas'
rutaGlobal = getcwd()+'/pruebas'


def ls(ruta):
    return listdir(ruta)


archivos = ls(rutaGlobal)

for archivo in archivos:
    ruta = rutaGlobal+"/"+archivo
    fp = open(ruta, "r")
    content = fp.read()
    lexer.input(content)
    fp.close()

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
