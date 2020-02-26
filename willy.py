import sys
from files import readFile


try:
    # Si el usuario suministra el archivo como un argumento
    if len(sys.argv) == 2:
        path = sys.argv[1]
        # Llama a la funcion readFile de files.py
        readFile(path)
    # Si el usuario no suministra el archivo como un argumento, el programa ofrece un prompt para que lo haga
    elif len(sys.argv) == 1:
        path = input("Archivo a interpretar: ")
        # Llama a la funcion readFile de files.py
        readFile(path)
# Si el archivo no existe, el programa termina indicando el problema
except FileNotFoundError:
    print("El archivo %s no existe" % path)
# Si el archivo no puede abrirse, el programa termina indicando el problema
except OSError:
    print("Imposible abrir el archivo %s" % path)
