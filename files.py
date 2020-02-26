import sys
from os import getcwd
from lexer import checkLexError
from wparser import parser, list_of_tasks, list_of_world, list_of_instr, checkContextError
from Print_functions import print_tarea, print_mundo, print_instr


def readFile(path):
    # obtener el directorio actual y concatenar con la direccion del archivo a abrir.
    rutaGlobal = getcwd()+"/"+path
    fp = open(rutaGlobal, "r")
    try:
        s = fp.read()
    except EOFError:
        pass
    result = parser.parse(s, tracking=True)
    # Si no tiene errores lexicograficos ni de contexto, entonces hace los prints finales
    if checkLexError() or checkContextError():
        sys.exit(0)
    print_tarea(list_of_tasks)
    print("\n")
    print_mundo(list_of_world)
    print_instr(list_of_instr)
    fp.close()