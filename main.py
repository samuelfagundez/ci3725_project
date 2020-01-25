import sys
from files import readFile

try:
    if len(sys.argv) == 2:
        path = sys.argv[1]
        readFile(path)
    elif len(sys.argv) == 1:
        path = input("Archivo a interpretar: ")
        readFile(path)
except:
    print("Imposible abrir el archivo %s" % path)
