import sys
from files import readFile


try:
    # Si el usuario suministra el archivo como un argumento
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        tarea = sys.argv[2]
        # Si el programa debe ejecutarse en manual
        if sys.argv[3] == "-m" or sys.argv[3] == "--manual":
            # Llama a la funcion readFile de files.py
            readFile(path, tarea, True, None)
        # Si el programa se ejecutara automaticamente
        elif sys.argv[3] == "-a" or sys.argv[3] == "--auto":
            # Verifica si el usuario ingreso la cantidad de segundos por instruccion
            if len(sys.argv) == 5:
                if int(sys.argv[4]) >= 0:
                    # Llama a la funcion readFile de files.py
                    readFile(path, tarea, False, int(sys.argv[4]))
            else:
                # Llama a la funcion readFile de files.py
                readFile(path, tarea, False, 0)
    # Si el usuario no suministra el archivo como un argumento, el programa ofrece un prompt para que lo haga
    elif len(sys.argv) == 1:
        temp = input("Archivo a interpretar, seguido de tarea a ejecutar y modalidad: ")
        temp = temp.split()
        path = temp[0]
        tarea = temp[1]
        # Si el programa debe ejecutarse en manual
        if temp[2] == "-m" or temp[2] == "--manual":
            # Llama a la funcion readFile de files.py
            readFile(path, tarea, True, None)
        # Si el programa se ejecutara automaticamente
        elif temp[2] == "-a" or temp[2] == "--auto":
            # Verifica si el usuario ingreso la cantidad de segundos por instruccion
            if len(temp) == 4:
                if int(temp[3]) >= 0:
                    # Llama a la funcion readFile de files.py
                    readFile(path, tarea, False, int(temp[3]))
            else:
                # Llama a la funcion readFile de files.py
                readFile(path, tarea, False, 0)

# Si el archivo no existe, el programa termina indicando el problema
except FileNotFoundError:
    print("El archivo %s no existe" % path)
# Si el archivo no puede abrirse, el programa termina indicando el problema
except OSError:
    print("Imposible abrir el archivo %s" % path)
except IndexError:
    print("Hubo un error en los argumentos colocados")
except RecursionError:
    print("Error Desconocido: Al parecer el programa es muy largo y Python no pudo seguir con la recursion")