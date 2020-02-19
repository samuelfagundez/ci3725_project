from BinTree import BinaryTree


class Instrucciones():
    def __init__(self, id, instruccion, arbol=None):
        self.id = id
        self.instruccion = instruccion
        if(arbol != None):
            self.arbol = arbol
        else:
            self.arbol = BinaryTree()
