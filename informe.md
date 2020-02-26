### Informe 2

##### Etapa Parser: Construimos el Parser utilizando Python, se utilizan los siguientes archivos:
###### - Casilla.py
###### - files.py
###### - Func.py
###### - lexer.py
###### - Print_functions.py
###### - Tabla_simbolos.py
###### - Task.py
###### - willy.py
###### - World.py
###### - wparser.py


###### En el archivo Casilla.py se define una clase llamada Casilla de la cual se crea una instancia de ella para cada casilla de un mundo, esto para guardar toda la información importante que pueda tener una casilla. Esta Información es: coordenada de posición, tipos de objetos con sus cantidades que se encuentran en la casilla y un booleano que indica si la casilla es una pared o no.

###### El archivo files.py tiene como propósito abrir el archivo donde se encuentra el programa y correr el parser definido por nosotros. Luego de que suceda esto, checkea si no ocurrió ningún error durante el parseo y se encarga de las llamadas a las funciones que imprimen el resultado de esta Entrega.

###### En el archivo Func.py se define una clase llamada Func de la cual se crea una instancia de ella para cada instrucción definida en una tarea (Task), esto para guardar toda la información importante que pueda tener una instrucción junto con su AST. Esta información es: Identificador de la instrucción, número de bloque asignado a esta instrucción y número de bloque donde fue definida esta instrucción.

###### En el archivo lexer.py se encuentra el analizador léxico de nuestro lenguaje. Obviaremos la explicación de él en este informe ya que este se encuentra en el informe de la Entrega 1.

###### En el archivo Print_functions.py se encuentran todas las funciones que sirven para hacer print de los resultados para esta entrega 2. Dos de estas funciones trabajan de manera recursiva para hacer más fácil el trabajo de imprimir todo con identación constante, en especial el AST de una tarea o instrucción definida.

###### En el archivo Tabla_simbolos.py se define la tabla de símbolos que se utilizara para los análisis de contexto. Esta tabla tendrá forma de pila en la cual empilaremos y desempilaremos en el tope las instrucciones definidas y las distintas variables definidas en un mundo por el usuario. Aparte de esto se hizo posible la búsqueda, usando el identificador, de estos símbolos en la tabla por medio de un ciclo que la recorre y regresa si existe y que tipo de variable es definida por este identificador. 

###### En el archivo Task.py se define una clase llamada Task de la cual se crea una instancia de ella para cada tarea que se defina en el programa, esto para guardar toda la información importante que pueda tener la tarea junto con su AST. Esta información es: Identificador de la tarea, Identificador del mundo en el que se ejecuta la tarea y número de bloque asignado.

###### En el archivo willy.py se encuentra el programa principal que obtendrá los argumentos desde la consola del usuario y dará inicio a la ejecución del programa. Obviaremos la explicación de él en este informe ya que este se encuentra en el informe de la Entrega 1.

###### En el archivo World.py se define una clase llamada World de la cual se crea una instancia de ella para cada mundo que se defina en el programa, esto para guardar toda la información importante que pueda tener el mundo junto con las variables que se definen en él. Esta información es: Identificador del mundo, lista de objetos con sus colores definidos en el mundo, lista de paredes que se encuentran en el mundo, capacidad de la bolsa de willy en el mundo, el grid del mundo representado como una matriz donde cada casilla contiene una instancia de la clase Casilla, dimensión del mundo, lista de objetos en la bolsa de willy, posición actual de willy en el mundo, lista de booleanos con sus valores definidos en el mundo, lista de objetivos definidos en el mundo y objetivo final del mundo. Cada método de esta clase devuelve True si la operación fue realizada con éxito o un string si ocurrió un error, donde el string da información acerca del error que ocurrió. Para guardar el objetivo final, el método definido para esto pide como argumento un árbol que define la expresión del objetivo final, este es recorrido usando DFS y generamos una lista ordenada de la expresión para así iterar por cada uno de los elementos y revisar si los elementos que la componen son objetivos previamente definidos o Booleanos definidos en el mundo. 