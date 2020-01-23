import sys
from files import readFile

if len(sys.argv) == 2:
    readFile(sys.argv[1])
elif len(sys.argv) == 1:
    path = input("Archivo a interpretar: ")
    readFile(path)
