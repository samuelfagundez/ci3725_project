class Casilla():

    def __init__(self, columna, fila, parent=None):
        self.columna = columna
        self.fila = fila
        self.objetos = {}
        self.pared = False

    def getCoordenada(self):
        return columna, fila

    def setObjeto(self, identificador, n):
        if identificador in self.objetos:
            self.objetos[identificador] += n
        self.objetos[identificador] = n

    def getObjeto(self, identificador):
        if identificador in self.objetos:
            return self.objetos[identificador]
        return 0

    def setPared(self):
        self.pared = True

    def getPared(self):
        return self.pared