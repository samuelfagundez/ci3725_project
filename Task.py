from BinTree import Nodo
from BinTree import BinaryTree


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

    def executeInstruction(self, cond, instruction1, instruction2):
        if(cond):
            instruction1()
            return True
        elif(instruction2):
            instruction2()
            return True

    def repeatNInstructions(self, n, instruction):
        localN = n
        while True:
            try:
                while(n):
                    instruction()
                    localN = localN - 1
            except:
                print("Error con la instruccion")
                exit(1)
            exit(0)

    def repeatInstruction(self, test, instruction):
        while True:
            try:
                while(test):
                    instruction()
            except:
                print("Error con la instruccion")
                exit(1)
            exit(0)
