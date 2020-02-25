
# Para cada Task que se defina en el programa, se creara una instancia de esta clase
# que guardara la informacion necesaria del Task
class Task():
    def __init__(self, identificador, worldId, parent=None):
        self.id = identificador
        self.worldId = worldId
        self.arbol = None

    # Asignamos el numero de bloque de este Task
    def setBloqNum(self, n):
        self.bloqNum = n

    # Obtenemos el numero de bloque de este Task
    def getBloqNum(self):
        return self.bloqNum

    # Asigna el AST del Task
    def setAST(self, arbol):
        self.arbol = arbol

    # Obtiene el AST del Task
    def getAST(self):
        return self.arbol
    
    # Obtiene el identificador del Task
    def getId(self):
        return self.id
    
    # Obtiene el identificador del mundo donde opera el Task
    def getWorldId(self):
        return self.worldId
