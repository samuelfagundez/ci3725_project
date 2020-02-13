
class Task():
    def __init__(self, identificador, worldId, parent=None):
        self.id = identificador
        self.worldId = worldId
        self.arbol = None

    def setArbolRecursivoInstr(self, arbol):
        self.arbol = arbol

    def getArbolRecursivoInstr(self):
        return self.arbol
    
    def getId(self):
        return self.id
    
    def getWorldId(self):
        return self.worldId