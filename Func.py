
# Para cada Instruccion definida en una Tarea, se crea una instancia de esta clase que
# guarda la informacion necesaria de la instruccion
class Func():
    def __init__(self, identificador, instr, n, m, parent=None):
        self.id = identificador
        self.instr = instr
        self.bloqNum = n 
        self.bloqEncontrado = m

    # Obtiene el identificador de la instruccion
    def getId(self):
        return self.id

    # Obtiene la instruccion de la instruccion
    def getInstr(self):
        return self.instr
    
    # Obtiene el num. de bloque de la instruccion
    def getBloqNum(self):
        return self.bloqNum

    # Obtiene el num. de bloque en el que fue definida la instruccion
    def getBloqEncontrado(self):
        return self.bloqEncontrado

    # Checkea si el Identificador esta siendo usado
    # Tambien devuelve para que esta siendo usado:
    # 0: Ninguno, 1: Objeto, 2: Booleano, 3: Objetivo, 4: Instruccion
    def checkId(self, id):
        if self.id == id:
            return True, 4
        return False, 0