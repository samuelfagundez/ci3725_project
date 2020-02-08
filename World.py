from casilla import Casilla

class World():
    def __init__(self, identificador, parent=None):

        self.id = identificador
        self.objects = {}
        self.walls = []
        self.basketCapacity = 1
        self.world = [[Casilla(1, 1)]]
        self.columnas = 1
        self.filas = 1
        self.willyBasket = {}
        self.willyPos = (1, 1, 'north')
        # Diccionario de booleanos donde la llave sera el identificador y el valor sera el valor actual del booleano.
        self.booleanos = {}
        # Goals. El primer valor de cada llave es el tipo de objetivo (0: posicion, 1: obj. En bolsa, 2: obj. En celda)
        # Los siguientes son especificos para cada tipo de objetivo.
        self.objetivos = {}


    # Crea el grid del mundo con sus casillas
    def newWorld(self, columnas, filas):
        
        if (columnas == 0) or (filas == 0):
            return "No se puede definir un mundo con 0 filas o 0 columnas"

        self.columnas = columnas
        self.filas = filas

        self.world = []
        for i in range(columnas):
            self.world.append([])
            for j in range(filas):
                # Para casa espacio, creamos una instancia de Casilla
                # que tendra la informacion de la casilla
                self.world[i].append(Casilla(i+1, j+1))


    # Obtiene las dimensiones del mundo
    def worldDim(self):

        return self.columnas, self.filas


    # Crea una nueva pared en el mundo
    def newWall(self, dir, columna0, fila0, columna1, fila1):

        # Estos if no se si colocarlos aqui o en el parser
        # Si las columnas estan por fuera del mundo, retorna error
        if (columna0 > self.columnas) or (columna1 > self.columnas) or (fila0 > self.filas) or (fila1 > self.filas):
            return "La columna(s) o fila(s) estan por afuera de las dimensiones del mundo."

        # Si no corresponde la direccion con las columnas/filas, retorna error
        if (dir == "east") and (columna0 - columna1 <= 0) and (fila0 == fila1):
            for i in range(columna0-1, columna1):
                self.world[i][fila0-1].setPared()

        elif (dir == "west") and (columna0 - columna1 >= 0) and (fila0 == fila1):
            for i in range(columna1-1, columna0):
                self.world[i][fila0-1].setPared()

        elif (dir == "south") and (columna1 == columna0) and (fila0 - fila1 >= 0):
            for i in range(fila1-1, fila0):
                self.world[columna0-1][i].setPared()

        elif (dir == "north") and (columna1 == columna0) and (fila0 - fila1 <= 0):
            for i in range(fila0-1, fila1):
                self.world[columna0-1][i].setPared()

        else:
            return "La direccion de la pared no concuerda."

        # Coloca la pared en la lista de paredes del mundo. Creo que esto no es necesario!!!!!!!!!!!!
        self.walls.append((dir, columna0, fila0, columna1, fila1))
        return True


    # Checkea si la casilla contiene una pared
    def isWallInCell(self, columna, fila):

        if (columna > self.columnas) or (fila > self.filas):
            return "La columna o fila estan por afuera de las dimensiones del mundo."

        return self.world[columna-1][fila-1].getPared()


    # Crea un nuevo tipo de objeto en el mundo
    def newObject(self, identificador, color):

        if identificador not in self.objects:
            self.objects[identificador] = color
            return True
        else:
            return "No se puede definir dos tipos de objeto con el mismo identificador en un mismo mundo."
    

    # Checkea si el objeto es valido en el mundo
    def isObjectValid(self, identificador):

        return identificador in self.objects


    # Busca el color del tipo de objeto en la lista de objetos del mundo
    def searchColorOfObject(self, identificador):

        if identificador in self.objects:
            return self.objects[identificador]
        else:
            return "El tipo de objeto no existe en este mundo."


    # Coloca un objeto en una casilla del mundo
    def placeInWorld(self, num, identificador, columna, fila):

        if num <= 0:
            return "El numero de objetos a colocar debe ser mayor que 0."
        elif identificador not in self.objects:
            return "El tipo de objeto no existe en este mundo."
        elif (columna > self.columnas) or (fila > self.filas):
            return "La columna o fila esta por afuera de las dimensiones del mundo."

        self.world[columna-1][fila-1].setObjeto(identificador, num)
        return True
    

    # Obtiene la cantidad de un tipo de objeto en una celda
    def getNumOfObjectInCell(self, identificador, columna, fila):

        if (columna > self.columnas) or (fila > self.filas):
            return "La columna o fila esta por afuera de las dimensiones del mundo."
        elif identificador not in self.objects:
            return "El tipo de objeto no existe en este mundo."

        return self.world[columna-1][fila-1].getObjeto(identificador)     # Si devuelve 0, debe generar un error!!!!!!!!!!!!!!!


    # Coloca un objeto en la cesta de Willy
    def placeInBasket(self, num, identificador):

        if num <= 0:
            return "El numero de objetos a crear debe ser mayor que 0."
        elif identificador not in self.objects:
            return "El tipo de objeto no existe en este mundo."
        elif sum(self.willyBasket) + num > self.basketCapacity:
            return "No se puede poner objeto en cesta ya que sobrepasa la capacidad maxima."

        # Si el objeto no esta en la cesta se agrega. Si ya esta, se agregan mas
        if identificador in self.willyBasket:
            self.willyBasket[identificador] += num
        else:
            self.willyBasket[identificador] = num
        return True


    # Obtiene la cantidad de un tipo de objeto en una celda
    def getNumOfObjectInBasket(self, identificador):

        if identificador not in self.objects:
            return "El tipo de objeto no existe en este mundo."

        if identificador in self.willyBasket:
            return self.willyBasket[identificador]
        return 0                                                      # Cuando pase esto, debe generar un error!!!!!!!!!!!!!!!


    # Asigna la capacidad de la bolsa de Willy
    def setCapacityOfBasket(self, n):

        if n <= 0:
            return "La capacidad de la bolsa debe ser mayor que 0."
        self.basketCapacity = n
        return True
    

    # Obtiene la capacidad de la bolsa de Willy
    def getCapacityOfBasket(self):
        return self.basketCapacity


    # Asigna casilla y direccion en donde willy estara ubicado inicialmente 
    def willyStartAt(self, columna, fila, direccion):

        if (columna > self.columnas) or (fila > self.filas):
            return "La columna o fila esta por afuera de las dimensiones del mundo."

        self.willyPos = (columna, fila, direccion)
        return True

    # Faltan los modulos para mover a willy, pero no se si esos van para esta entrega!!!!!!!!!!


    # Define un nuevo booleano en el mundo
    def newBoolean(self, identificador, valor):

        if identificador in self.booleanos:
            return "No se puede definir dos booleanos con el mismo identificador en un mismo mundo."
        
        self.booleanos[identificador] = valor
        return True

    
    # Checkea si el booleano existe en el mundo
    def isBooleanValid(self, identificador):

        return identificador in self.booleanos


    # Obtiene el valor actual del booleano
    def getBoolean(self, identificador):

        if identificador not in self.booleanos:
            return "El Booleano no esta definido en el mundo."
        else:
            self.booleanos[identificador]


    # Actualiza el valor de un booleano que ya existe en el mundo
    def setBoolean(self, identificador, valor):

        if identificador not in self.booleanos:
            return "El Booleano no esta definido en el mundo."

        self.booleanos[identificador] = valor
        return True


    # Define un objetivo del tipo posicion de Willy
    def setGoalPosWilly(self, identificador, columna, fila):

        if identificador in self.objetivos:
            return "No se puede definir dos objetivos con el mismo identificador en el mismo mundo."

        self.objetivos[identificador] = (0, columna, fila)
        return True


    # Define un objetivo del tipo objeto en bolsa de Willy
    def setGoalObjBasket(self, identificador, n, idObj):

        if identificador in self.objetivos:
            return "No se puede definir dos objetivos con el mismo identificador en el mismo mundo."

        self.objetivos[identificador] = (1, n, idObj)
        return True


    # Define un Objetivo del tipo objeto en casillo
    def setGoalObjCelda(self, identificador, n, idObj, columna, fila):

        if identificador in self.objetivos:
            return "No se puede definir dos objetivos con el mismo identificador en el mismo mundo."

        self.objetivos[identificador] = (2, n, idObj, columna, fila)
        return True

    
    # Obtiene el objetivo deseado
    def getGoal(self, identificador):

        if identificador in self.objetivos:
            return "No se existe un objetivo en el mundo con ese identificador."

        return self.objetivos[identificador]


    # Define el objetivo final del mundo. Puede que cambie esto, no creo que se haga asi!!!!!!!
    def setFinalGoal(self, goals):

        self.objetivoFinal = goals
        return True

    
    # Obtiene el objetivo final del mundo
    def getFinalGoal(self):

        return self.objetivoFinal