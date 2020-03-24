import sys
from os import getcwd
from lexer import checkLexError
from wparser import parser, list_of_tasks, list_of_world, list_of_instr, checkContextError
from execute import execute


def readFile(path, tarea, mod, segundos):
    # obtener el directorio actual y concatenar con la direccion del archivo a abrir.
    rutaGlobal = getcwd()+"/"+path
    fp = open(rutaGlobal, "r")
    try:
        s = fp.read()
    except EOFError:
        pass
    result = parser.parse(s, tracking=True)
    # Si no tiene errores lexicograficos ni de contexto, entonces ejecuta el programa
    if checkLexError() or checkContextError():
        sys.exit(0)
    # Ejecuta el programa
    execute(list_of_tasks, list_of_world, list_of_instr, tarea, mod, segundos)
    fp.close()