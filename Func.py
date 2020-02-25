
# Para cada funcion definida en una Tarea, se crea una instancia de esta clase que
# guarda la informacion necesaria de la funcion
class Func():
    def __init__(self,id, instr, n, m, parent=None):
        self.id = id
        self.instr = instr
        self.bloqNum = n 
        self.bloqEncontrado = m

    # Obtiene el identificador de la funcion
    def getId(self):
        return self.id

    # Obtiene la instruccion de la Funcion
    def getInstr(self):
        return self.instr
    
    # Obtiene el num. de bloque de la funcion
    def getBloqNum(self):
        return self.bloqNum

    # Obtiene el num. de bloque en el que fue definida la funcion
    def getBloqEncontrado(self):
        return self.bloqEncontrado

    # Checkea si el Identificador esta siendo usado
    # Tambien devuelve para que esta siendo usado:
    # 0: Ninguno, 1: Objeto, 2: Booleano, 3: Objetivo, 4: Funcion
    def checkId(self, id):
        if self.id == id:
            return True, 4
        return False, 0