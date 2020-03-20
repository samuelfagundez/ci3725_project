
class TSimbolos():
    def __init__(self, parent=None):
        self.pila = []

    # Insertar en la tabla de simbolos
    def insert(self, data):
        for i in range(len(self.pila)):
            if data.getId() == self.pila[i].getId():
                return "No se puede definir mas de una instruccion con el mismo nombre"
        # Lo agrega en el tope de la tabla
        self.pila.append(data)
        return True

    # Obtiene el num. de bloque de la tabla al tope de la pila. Si esta vacia
    def getTopBloqNum(self):
        if len(self.pila) == 0:
            return 0
        return self.pila[-1].getBloqNum()

    # Desempila en la tabla de simbolos
    def pop(self):
        # No se puede desempilar una tabla de un Stack vacio.
        if len(self.pila) == 0:
            return None
        return self.pila.pop()

    # Checkea si la tabla esta vacia
    def empty(self):
        if len(self.pila) == 0:
            return True
        return False

    # Checkea si existe el simbolo de tipo "type" en la tabla de simbolos
    # Para esta entrega (Entrega 2) nos limitamos a decir que existe o no en la tabla
    def find(self, simbolo, type):
        for i in range(len(self.pila)):
            simbolo_check = self.pila[i].checkId(simbolo)
            if(simbolo_check == (True, 1)) and (type == "objects"):
                return True
            elif(simbolo_check == (True, 2)) and (type == "boolean"):
                return True
            elif(simbolo_check == (True, 3)) and (type == "objetivos"):
                return True
            elif(simbolo_check == (True, 4)) and (type == "func"):
                return True
        return False