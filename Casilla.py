
# Para cada casilla de un mundo se crea una instancia de esta clase que guarda
# la informacion necesaria de la Casilla
class Casilla():
    def __init__(self, columna, fila, parent=None):
        self.columna = columna
        self.fila = fila
        self.objetos = {}
        self.pared = False

    # Obtiene la coordenada de la Casilla
    def getCoordenada(self):
        return self.columna, self.fila

    # Coloca un objeto en la casilla
    def setObjeto(self, identificador, n):
        
        if identificador in self.objetos.keys():
            self.objetos[identificador] += n
        else:
            self.objetos[identificador] = n

    # Obtiene el num. de objetos en la casilla del mismo tipo, dado por identificador
    def getObjeto(self, identificador):
        if identificador in self.objetos.keys():
            return self.objetos[identificador]
        return 0

    # Quita una instancia de el tipo de objeto de la casilla
    def pickObjeto(self, identificador):
        self.objetos[identificador] -= 1
        if self.objetos[identificador] <= 0:
            del self.objetos[identificador]

    # Obtiene el num. de objetos totales en esta casilla
    def getNumObjetos(self):
        return sum(self.objetos.values())

    # Obtiene todos los objetos de la casilla (Lo uso solo para los prints
    # de la entrega 2, puede que lo elimine luego)
    def getAllObjetos(self):
        return self.objetos

    # Agrega una pared en la casilla
    def setPared(self):
        self.pared = True

    # Chekea si la casilla tiene una pared
    def getPared(self):
        return self.pared