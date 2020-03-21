from Casilla import Casilla
import sys

class World():
    def __init__(self, identificador, parent=None):

        # Identificador del mundo
        self.id = identificador
        # Lista de objetos definidos en el mundo
        self.objects = {}
        # Lista de paredes con sus coordenadas en el mundo
        self.walls = []
        # Capacidad de Basket del mundo
        self.basketCapacity = 1
        # Grid del mundo
        self.world = [[Casilla(1, 1)]]
        # Num. de Columnas del mundo
        self.columnas = 1
        # Num. de Filas del mundo
        self.filas = 1
        # Lista de objetos que estan en la bolsa de Willy
        self.willyBasket = {}
        # Posicion de Willy en el mundo
        self.willyPos = [0, 0, 'north']
        # Diccionario de booleanos donde la llave sera el identificador y el valor sera el valor actual del booleano.
        self.booleanos = {}
        # Goals. El primer valor de cada llave es el tipo de objetivo (0: posicion, 1: obj. En bolsa, 2: obj. En celda)
        # Los siguientes son especificos para cada tipo de objetivo.
        self.objetivos = {}
        # Objetivo final del mundo
        self.objetivoFinal = None
        # Mantiene en un arreglo la cantidad de veces que se llaman a las instrucciones que solo pueden ser llamadas a lo sumo una vez
        # 0: World, 1: Start at, 2: Basket of capacity, 3: Final goal is
        self.instrucciones_unicas = [0, 0, 0, 0]


    def dfs(self, nodo, visited):
        if type(nodo) is not tuple:
            visited.append((nodo))
        if type(nodo) is tuple:
            for n in nodo:
                self.dfs(n, visited)
        return visited

    # Checkea si el Identificador esta siendo usado para distintos usos
    # Tambien devuelve para que esta siendo usado:
    # 0: Ninguno, 1: Objeto, 2: Booleano, 3: Objetivo, 4: Instruccion
    def checkId(self, id):
        if id in self.objects:
            return True, 1
        elif id in self.booleanos:
            return True, 2
        elif id in self.objetivos:
            return True, 3
        return False, 0

    # Asigna el num. de bloque del mundo
    def setBloqNum(self, n):
        self.bloqNum = n

    # Obtiene el num. de bloque del mundo
    def getBloqNum(self):
        return self.bloqNum
        
    # Crea el grid del mundo con sus casillas
    def newWorld(self, columnas, filas):
        
        # Ya no se puede volver a llamar la instruccion World en este mundo
        self.instrucciones_unicas[0] += 1
        if (columnas == 0) or (filas == 0):
            return "No se puede definir un mundo con 0 filas o 0 columnas"
        if(self.instrucciones_unicas[0] > 1):
            return "No se puede definir mas de una instruccion de este tipo por mundo"

        # Asigna el num. de columnas y filas del mundo
        self.columnas = columnas
        self.filas = filas

        # Genera el Grid donde cada casilla es una instancia de la clase Casilla
        # que contiene la informacion de ese espacio
        for i in range(columnas):
            if i != 0:
                self.world.append([])
            for j in range(filas):
                if (i != 0) or (j != 0):
                    self.world[i].append(Casilla(i+1, j+1))
        return True


    # Obtiene las dimensiones del mundo
    def getWorldDim(self):
        return self.columnas, self.filas

    # Obtiene el Identificador del mundo
    def getId(self):
        return self.id


    # Crea una nueva pared en el mundo
    def newWall(self, dir, columna0, fila0, columna1, fila1):

        # Si las columnas estan por fuera del mundo, retorna error
        if (columna0 > self.columnas) or (columna1 > self.columnas) or (fila0 > self.filas) or (fila1 > self.filas) or (columna0 == 0) or (fila0 == 0) or (columna1 == 0) or (fila1 == 0):
            return "La columna(s) o fila(s) estan por afuera de las dimensiones del mundo."

        # Si no corresponde la direccion con las columnas/filas, retorna error
        if (dir == "east") and (columna0 - columna1 <= 0) and (fila0 == fila1):
            for i in range(columna0-1, columna1):
                # Verificamos que no ocurre ningun error
                if self.world[i][fila0-1].getNumObjetos() > 0:
                    return "No se pueden colocar muros sobre casillas que tienen objetos"
                elif (self.willyPos[0] == i+1) and (self.willyPos[1] == fila0):
                    return "No se pueden colocar muros sobre Willy"
                # Colocamos pared en una de las casillas que comprende
                self.world[i][fila0-1].setPared()

        elif (dir == "west") and (columna0 - columna1 >= 0) and (fila0 == fila1):
            for i in range(columna1-1, columna0):
                # Verificamos que no ocurre ningun error
                if self.world[i][fila0-1].getNumObjetos() > 0:
                    return "No se pueden colocar muros sobre casillas que tienen objetos"
                elif (self.willyPos[0] == i+1) and (self.willyPos[1] == fila0):
                    return "No se pueden colocar muros sobre Willy"
                # Colocamos pared en una de las casillas que comprende
                self.world[i][fila0-1].setPared()

        elif (dir == "south") and (columna1 == columna0) and (fila0 - fila1 >= 0):
            for i in range(fila1-1, fila0):
                # Verificamos que no ocurre ningun error
                if self.world[columna0-1][i].getNumObjetos() > 0:
                    return "No se pueden colocar muros sobre casillas que tienen objetos"
                elif (self.willyPos[0] == columna0) and (self.willyPos[1] == i+1):
                    return "No se pueden colocar muros sobre Willy"
                # Colocamos pared en una de las casillas que comprende
                self.world[columna0-1][i].setPared()

        elif (dir == "north") and (columna1 == columna0) and (fila0 - fila1 <= 0):
            for i in range(fila0-1, fila1):
                # Verificamos que no ocurre ningun error
                if self.world[columna0-1][i].getNumObjetos() > 0:
                    return "No se pueden colocar muros sobre casillas que tienen objetos"
                elif (self.willyPos[0] == columna0) and (self.willyPos[1] == i+1):
                    return "No se pueden colocar muros sobre Willy"
                # Colocamos pared en una de las casillas que comprende
                self.world[columna0-1][i].setPared()

        else:
            return "La direccion de la pared no concuerda."

        # Coloca la pared en la lista de paredes del mundo.
        self.walls.append((dir, columna0, fila0, columna1, fila1))
        return True


    # Obtiene las paredes del mundo
    def getWalls(self):
        return self.walls


    # Checkea si la casilla contiene una pared
    def isWallInCell(self, columna, fila, direccion):
        if (columna > self.columnas) or (fila > self.filas) or (columna == 0) or (fila == 0):
            return "La columna o fila estan por afuera de las dimensiones del mundo."

        if direccion == "north" and columna-1 >= 0 and fila < self.filas:
            return self.world[columna-1][fila].getPared()
        elif direccion == "east" and columna < self.columnas and fila-1 >= 0:
            return self.world[columna][fila-1].getPared()
        elif direccion == "south"and columna-1 >=0 and fila-2 >= 0:
            return self.world[columna-1][fila-2].getPared()
        elif direccion == "west" and columna-2 >=0 and fila-1 >= 0:
            return self.world[columna-2][fila-1].getPared()
        elif direccion is None:
            return self.world[columna-1][fila-1].getPared()
        return True


    # Crea un nuevo tipo de objeto en el mundo
    def newObject(self, identificador, color):

        if identificador in self.objects:
            return "No se puede definir dos tipos de objeto con el mismo identificador en un mismo mundo."
        if self.checkId(identificador)[0]:
            return "No se puede utilizar el mismo identificador para distintos usos"

        self.objects[identificador] = color
        return True


    # Obtenemos todos los objetos del mundo
    def getObjetos(self):
        return self.objects


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
        if identificador not in self.objects:
            return "El tipo de objeto no existe en este mundo."
        if (columna > self.columnas) or (fila > self.filas) or (columna == 0) or (fila == 0):
            return "La columna o fila esta por afuera de las dimensiones del mundo."
        if self.isWallInCell(columna, fila, None):
            return "No se pueden colocar objetos sobre muros"

        self.world[columna-1][fila-1].setObjeto(identificador, num)
        return True
    

    # Obtiene la cantidad de un tipo de objeto en una celda
    def getNumOfObjectInCell(self, identificador, columna, fila):

        if (columna > self.columnas) or (fila > self.filas) or (columna == 0) or (fila == 0):
            return "La columna o fila esta por afuera de las dimensiones del mundo."
        if identificador not in self.objects:
            return "El tipo de objeto no existe en este mundo."

        return self.world[columna-1][fila-1].getObjeto(identificador)


    # Coloca un objeto en la cesta de Willy
    def placeInBasket(self, num, identificador):

        if num <= 0:
            return "El numero de objetos a poner en la bolsa de willy debe ser mayor que 0."
        if identificador not in self.objects:
            return "El tipo de objeto no existe en este mundo."
        if sum(self.willyBasket.values()) + num > self.basketCapacity:
            return "No se puede poner objeto en cesta ya que sobrepasa la capacidad maxima."

        # Si el objeto no esta en la cesta se agrega. Si ya esta, se agregan mas
        if identificador in self.willyBasket:
            self.willyBasket[identificador] += num
        else:
            self.willyBasket[identificador] = num
        return True


    # Obtiene la cantidad de un tipo de objeto en la bolsa de willy
    def getNumOfObjectInBasket(self, identificador):

        if identificador not in self.objects:
            return "El tipo de objeto no existe en este mundo."

        if identificador in self.willyBasket:
            return self.willyBasket[identificador]
        return 0                      


    # Obtiene la bolsa de willy
    def getBasket(self):
        return self.willyBasket                       


    # Asigna la capacidad de la bolsa de Willy
    def setCapacityOfBasket(self, n):
        
        # Ya no se puede volver a llamar la instruccion Basket of capacity en este mundo
        self.instrucciones_unicas[2] += 1
        if n <= 0:
            return "La capacidad de la bolsa debe ser mayor que 0."
        if(self.instrucciones_unicas[2] > 1):
            return "No se puede definir mas de una instruccion de este tipo por mundo"
        self.basketCapacity = n
        return True
    

    # Obtiene la capacidad de la bolsa de Willy
    def getCapacityOfBasket(self):
        return self.basketCapacity


    # Asigna casilla y direccion en donde willy estara ubicado inicialmente 
    def willyStartAt(self, columna, fila, direccion):
        
        if (columna > self.columnas) or (fila > self.filas) or (columna == 0) or (fila == 0):
            return "La columna o fila esta por afuera de las dimensiones del mundo."
        if self.isWallInCell(columna, fila, None):
            return "No se puede colocar a willy sobre muros"
        # Ya no se puede volver a llamar la instruccion Start at en este mundo
        self.instrucciones_unicas[1] += 1
        if(self.instrucciones_unicas[1] > 1):
            return "No se puede definir mas de una instruccion de este tipo por mundo"

        self.willyPos = [columna, fila, direccion]
        return True


    # Obtiene en cual casilla esta willy
    def getWillyPos(self):
        return self.willyPos[0], self.willyPos[1], self.willyPos[2]


    # Define un nuevo booleano en el mundo
    def newBoolean(self, identificador, valor):

        if identificador in self.booleanos:
            return "No se puede definir dos booleanos con el mismo identificador en un mismo mundo."
        if self.checkId(identificador)[0]:
            return "No se puede utilizar el mismo identificador para distintos usos"
        
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
            return self.booleanos[identificador]


    # Obtiene todos los booleanos del mundo
    def getAllBoolean(self):
        return self.booleanos


    # Define un objetivo del tipo posicion de Willy
    def setGoalPosWilly(self, identificador, columna, fila):

        if identificador in self.objetivos:
            return "No se puede definir dos objetivos con el mismo identificador en el mismo mundo."
        if self.checkId(identificador)[0]:
            return "No se puede utilizar el mismo identificador para distintos usos"
        if (columna > self.columnas) or (fila > self.filas) or (columna == 0) or (fila == 0):
            return "La columna o fila esta por afuera de las dimensiones del mundo."

        self.objetivos[identificador] = (0, columna, fila)
        return True


    # Define un objetivo del tipo objeto en bolsa de Willy
    def setGoalObjBasket(self, identificador, n, idObj):

        if identificador in self.objetivos:
            return "No se puede definir dos objetivos con el mismo identificador en el mismo mundo."
        if self.checkId(identificador)[0]:
            return "No se puede utilizar el mismo identificador para distintos usos"
        if idObj not in self.objects:
            return "La condicion espera un identificador de tipo objeto."

        self.objetivos[identificador] = (1, n, idObj)
        return True


    # Define un Objetivo del tipo objeto en casillo
    def setGoalObjCelda(self, identificador, n, idObj, columna, fila):
        
        if identificador in self.objetivos:
            return "No se puede definir dos objetivos con el mismo identificador en el mismo mundo."
        if self.checkId(identificador)[0]:
            return "No se puede utilizar el mismo identificador para distintos usos"
        if idObj not in self.objects:
            return "La condicion espera un identificador de tipo objeto."
        if (columna > self.columnas) or (fila > self.filas) or (columna == 0) or (fila == 0):
            return "La columna o fila esta por afuera de las dimensiones del mundo."
            
        self.objetivos[identificador] = (2, n, idObj, columna, fila)
        return True

    
    # Obtiene el objetivo deseado
    def getGoal(self, identificador):

        if identificador not in self.objetivos.keys():
            return "No se existe un objetivo en el mundo con este identificador."

        return self.objetivos[identificador]


    # Obtiene todos los objetivos de este mundo
    def getAllGoals(self):
        return self.objetivos


    # Define el objetivo final del mundo.
    def setFinalGoal(self, goals):
        
        # Ya no se puede volver a llamar la instruccion Final Goal is en este mundo
        self.instrucciones_unicas[3] += 1
        if(self.instrucciones_unicas[3] > 1):
            return "No se puede definir mas de una instruccion de este tipo por mundo"
        # Revisamos si las condiciones puestas en el objetivo final son objetivos ya definidos
        # o son Booleanos
        temp = self.dfs(goals, [])
        for i in range(len(temp)):
            if (temp[i] != "and") and (temp[i] != "or") and (temp[i] != "not"):
                if (temp[i] not in self.objetivos) and (temp[i] not in self.booleanos):
                    return "Las condiciones en el objetivo final deben ser objetivos definidos o booleanos"

        self.objetivoFinal = goals
        return True

    
    # Obtiene el objetivo final del mundo
    def getFinalGoal(self):
        return self.objetivoFinal


    # Mueve a willy en el mundo
    def move(self):

        if self.willyPos[2] == "north" and self.willyPos[1] != self.filas:
            self.willyPos[1] += 1 
            return True
        elif self.willyPos[2] == "south" and self.willyPos[1] > 1:
            self.willyPos[1] -= 1 
            return True
        elif self.willyPos[2] == "west" and self.willyPos[0] > 1:
            self.willyPos[0] -= 1 
            return True
        elif self.willyPos[2] == "east" and self.willyPos[0] != self.columnas:
            self.willyPos[0] += 1 
            return True
        return False


    # Voltea a willy hacia la izquierda
    def turnLeft(self):

        if self.willyPos[2] == "north":
            self.willyPos[2] = "west"
        elif self.willyPos[2] == "west":
            self.willyPos[2] = "south"
        elif self.willyPos[2] == "south":
            self.willyPos[2] = "east"
        elif self.willyPos[2] == "east":
            self.willyPos[2] = "north"
    

    # Voltea a willy hacia la derecha
    def turnRight(self):
        
        if self.willyPos[2] == "north":
            self.willyPos[2] = "east"
        elif self.willyPos[2] == "east":
            self.willyPos[2] = "south"
        elif self.willyPos[2] == "south":
            self.willyPos[2] = "west"
        elif self.willyPos[2] == "west":
            self.willyPos[2] = "north"
    

    # Actualiza el valor de un booleano que ya existe en el mundo
    def setBoolean(self, identificador, valor):
        self.booleanos[identificador] = valor


    # Coloca un objeto de la casilla en la bolsa de willy
    def pick(self, identificador):
        
        if self.getNumOfObjectInCell(identificador, self.getWillyPos()[0], self.getWillyPos()[1]) <= 0:
            return "No existe un objeto de tipo '" + identificador + "' en la casilla (" + str(self.getWillyPos()[0]) + ", " + str(self.getWillyPos()[1]) + ")."
        if sum(self.willyBasket.values()) == self.basketCapacity:
            return "La bolsa de Willy esta llena y no se pueden recoger mas objetos."
        
        # Recogemos de la casilla el objeto
        self.world[self.getWillyPos()[0]-1][self.getWillyPos()[1]-1].pickObjeto(identificador)
        # Lo colocamos en la cesta
        self.placeInBasket(1, identificador)
        return None


    # Suelta un objeto de la bolsa en la casilla en la que se encuentre willy
    def drop(self, identificador):

        if identificador not in self.willyBasket.keys():
            return "No existe un objeto de tipo '" + identificador + "' en la bolsa de willy."
        
        # Recogemos el objeto de la bolsa de willy
        self.willyBasket[identificador] -= 1
        if self.willyBasket[identificador] <= 0:
            del self.willyBasket[identificador]
        # Lo dejamos en la casilla en la que estemos
        self.placeInWorld(1, identificador, self.getWillyPos()[0], self.getWillyPos()[1])
        return None