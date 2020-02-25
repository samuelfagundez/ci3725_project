# DFS modificado para recorrer el AST
def dfs(nodo, visited):
    if type(nodo) is not tuple:
        visited.append((nodo))
    if type(nodo) is tuple:
        for n in nodo:
            dfs(n, visited)
    return visited

#########################################################################
#                      Funciones para imprimir                          #
#########################################################################

# Funcion llamada por print_recursive para imprimir la condicion de las
# instrucciones if y while
def print_recursive_cond(arbol, j, num_ident):
    if arbol[j] == "and" or arbol[j] == "or":
        if arbol[j] == "and":
            print("  "*num_ident + "CONJUNCION:")
        else:
            print("  "*num_ident + "DISYUNCION:")
        num_ident += 1
        print("  "*num_ident + "lado izquierdo:")
        j = print_recursive_cond(arbol, j+1, num_ident+1)
        print("  "*num_ident + "lado derecho:")
        j = print_recursive_cond(arbol, j, num_ident+1)

    elif arbol[j] == "not":
        print("  "*num_ident + "NEGADO:")
        j = print_recursive_cond(arbol, j+1, num_ident+1)

    else:
        if (arbol[j] == "carrying") or (arbol[j] == "found"):
            print("  "*num_ident+ str(arbol[j]) + "(" + str(arbol[j+1]) + ")")
            j += 2
        else:
            print("  "*num_ident + str(arbol[j]))
            j += 1 
    return j


# Funcion recursiva para imprimir el arbol
def print_recursive(arbol, j, num_ident):
    if (arbol[j] == "if") or (arbol[j] == "while"):
        if arbol[j] == "if":
            print("  "*num_ident + "IF:")
        else:
            print("  "*num_ident + "CICLO WHILE:")
        num_ident += 1
        print("  "*num_ident + "condicion:")
        num_ident += 1
        # Imprimimos la condicion
        j = print_recursive_cond(arbol, j+1, num_ident)
        # Imprimimos la instruccion 
        print("  "*(num_ident-1) + "instruccion:")
        j = print_recursive(arbol, j, num_ident)
        # Si la instruccion IF es seguida por un ELSE, se ejecuta lo siguiente
        if len(arbol) > j:
            num_ident -= 2
            if arbol[j] == "else":
                j += 1
                print("  "*num_ident + "ELSE:")
                j = print_recursive(arbol, j, num_ident+1)
    elif arbol[j] == "pick":
        print("  "*num_ident + "PICK: " + arbol[j+1])
        j += 2
    elif arbol[j] == "drop":
        print("  "*num_ident + "DROP: " + arbol[j+1])
        j += 2
    elif arbol[j] == "set":
        if arbol[j+2] == "to":
            j += 4
            print("  "*num_ident + "SET: " + arbol[j-3] + " TO: " + str(arbol[j-1]))
        else:
            j += 2
            print("  "*num_ident + "SET: " + arbol[j-1])
    elif arbol[j] == "clear":
        print("  "*num_ident + "CLEAR: " + arbol[j+1])
        j += 2
    elif arbol[j] == "flip":
        print("  "*num_ident + "FLIP: " + arbol[j+1])
        j += 2
    elif arbol[j] == "repeat":
        j += 2
        print("  "*num_ident + "REPEAT " + str(arbol[j-1]) + ":")
        j = print_recursive(arbol, j, num_ident+1)
    elif (arbol[j] == "begin") or (arbol[j] == "end"):
        j += 1
        while arbol[j] != "end":
            j = print_recursive(arbol, j, num_ident)
        j += 1
    else:
        if arbol[j] != None:
            print("  "*num_ident + str(arbol[j]).upper())
        j += 1
    return j


# Funcion que imprime arbol de tareas
def print_tarea(list_tasks):
    print(" TAREAS:")
    for i in range(len(list_tasks)):
        # Numeros de identacion a dejar. Lo guardamos en variable para mantener
        # las identaciones constantes
        num_ident = 0
        tarea = list_tasks[i]
        print(tarea.getId() + ":")
        num_ident += 1
        print("  "*num_ident + "mundo: " + tarea.getWorldId())
        print("  "*num_ident + "identificador de bloque: " + str(tarea.getBloqNum()))
        print("  "*num_ident + "bloque de instrucciones:")
        num_ident += 1
        # Recorre el arbol y regresa una lista ordenada con las instrucciones del Task
        # Esta lista es usada en la funcion print_recursive que se encarga de imprimir el AST
        arbol = dfs(tarea.getAST(), [])
        # j: Iterador de elementos del arbol
        j = 0
        # Imprime el arbol en orden
        while j in range(len(arbol)):
            j = print_recursive(arbol, j, num_ident)
        print()


# Funcion que imprime cada instruccion definida en el programa
def print_instr(list_instr):
    print(" INSTRUCCIONES:")
    for i in range(len(list_instr)):
        # Numeros de identacion a dejar. Lo guardamos en variable para mantener
        # las identaciones constantes
        num_ident = 1
        instr = list_instr[i]
        print(instr.getId() + ":")
        print("  "*num_ident + "tipo: instruccion")
        print("  "*num_ident + "bloque de declaración: " + str(instr.getBloqEncontrado()))
        print("  "*num_ident + "número de bloque: " + str(instr.getBloqNum()))
        print("  "*num_ident + "ast asociado:")
        num_ident += 1
        arbol = dfs(instr.getInstr(), [])
        j = 0
        # Imprime el arbol en orden
        while j in range(len(arbol)):
            j = print_recursive(arbol, j, num_ident)
        print()


# Funcion que imprime arbol de tareas
def print_mundo(list_worlds):
    for i in range(len(list_worlds)):
        mundo = list_worlds[i]
        dim = mundo.getWorldDim()
        # Numeros de identacion a dejar. Lo guardamos en variable para mantener
        # las identaciones constantes
        num_ident = 0
        print(mundo.getId() + ":")
        num_ident += 1

        print("  "*num_ident + "tipo: mundo")
        print("  "*num_ident + "identificador de bloque: " + str(mundo.getBloqNum()))
        print("  "*num_ident + "tamanio: " + str(dim))
        print("  "*num_ident + "muros: ")
        num_ident += 1
        # Imprimimos muros del mundo
        muros = mundo.getWalls()
        for j in range(len(muros)):
            print("  "*num_ident + "- " + muros[j][0] + ", from " + str(muros[j][1]) + " " 
            + str(muros[j][2]) + " to " + str(muros[j][3]) + " " + str(muros[j][4])) 
        num_ident -= 1
        # Imprimimos objetos en el mundo
        print("  "*num_ident + "objetos en mundo: ")
        num_ident += 1
        for j in range(dim[0]):
            for k in range(dim[1]):
                objetosCasilla = mundo.world[j][k].getAllObjetos()
                for m in objetosCasilla:
                    print("  "*num_ident + "- " + str(objetosCasilla[m]) + " of " + m + " at " + 
                    str(j+1) + " " + str(k+1))
        num_ident -= 1
        # Imprimimos objetos en Bolsa
        print("  "*num_ident + "objetos en Basket: ")
        num_ident += 1
        basket = mundo.getBasket()
        for j in basket:
            print("  "*num_ident + "- " + str(basket[j]) + " of " + j)
        num_ident -= 1
        # Imprimimos donde empieza Willy
        wilPos = mundo.getWillyPos()
        print("  "*num_ident + "willy empieza en: " + str(wilPos[0]) + " " + str(wilPos[1]) +
        " heading " + str(wilPos[2]))
        # Imprime la capacidad de la bolsa de willy
        print("  "*num_ident + "capacidad de basket: " + str(mundo.getCapacityOfBasket()))
        # Imprime la Condicion con que termina el programa en este mundo
        print("  "*num_ident + "goal final:")
        num_ident += 1
        finalGoal = mundo.getFinalGoal()
        if mundo.getFinalGoal() != None:
            print_recursive_cond(dfs(finalGoal, []), 0, num_ident)
        num_ident -= 1
        # Ahora pasamos a imprimir las variables en este mundo
        print()
        # Tipo de objetos:
        objetos = mundo.getObjetos()
        for j in objetos:
            print(j + ":")
            print("  "*num_ident + "tipo: objeto")
            print("  "*num_ident + "color: " + objetos[j])
            print("  "*num_ident + "bloque de definicion: " + str(mundo.getBloqNum()))
            print()
        # Booleanos:
        booleanos = mundo.getAllBoolean()
        for j in booleanos:
            print(j + ":")
            print("  "*num_ident + "tipo: booleano")
            print("  "*num_ident + "valor: " + str(booleanos[j]))
            print("  "*num_ident + "bloque de definicion: " + str(mundo.getBloqNum()))
            print()
        # Objetivos
        objetivos = mundo.getAllGoals()
        for j in objetivos:
            print(j + ":")
            print("  "*num_ident + "tipo: objetivo")
            if objetivos[j][0] == 0:
                print("  "*num_ident + "valor: Willy esta en " + str(objetivos[j][1]) + " " + str(objetivos[j][2]))
            elif objetivos[j][0] == 1:
                print("  "*num_ident + "valor: " + str(objetivos[j][1]) + " " + str(objetivos[j][2]) + " objetos en Basket")
            else:
                print("  "*num_ident + "valor: " + str(objetivos[j][1]) + " " + str(objetivos[j][2]) + " objetos en " +
                str(objetivos[j][3]) + " " + str(objetivos[j][4]))
            print("  "*num_ident + "bloque de definicion: " + str(mundo.getBloqNum()))
            print()