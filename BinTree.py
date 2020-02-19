class Nodo:
    def __init__(self, nombre=None, id=None, izq=None, der=None):
        self.nombre = nombre
        self.id = id
        self.izq = izq
        self.der = der

    def __str__(self):
        return "%s %s" % (self.nombre, self.id)


class BinaryTree:
    def __init__(self):
        self.raiz = None

    def inorden(self, elemento):
        if elemento != None:
            self.inorden(elemento.izq)
            print(elemento)
            self.inorden(elemento.der)

    def getRoot(self):
        return self.raiz

    def insert(self, elemento):
        if(self.raiz == None):
            self.raiz = elemento
        else:
            aux = self.raiz
            padre = None
            while aux != None:
                padre = aux
                if (int(elemento.id) >= int(aux.id)):
                    aux = aux.der
                else:
                    aux = aux.izq
            if (int(elemento.id) >= int(padre.id)):
                padre.der = elemento
            else:
                padre.izq = elemento
