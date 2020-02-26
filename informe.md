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


En el archivo Casilla.py se define una clase llamada Casilla de la cual se crea una instancia para cada casilla de un mundo, esto para guardar toda la información importante que pueda tener una casilla. Esta Información es: coordenada de posición, tipos de objetos con sus cantidades que se encuentran en la casilla y un booleano que indica si la casilla es una pared o no.

El archivo files.py tiene como propósito abrir el archivo donde se encuentra el programa y correr el parser definido por nosotros. Luego de que suceda esto, checkea si no ocurrió ningún error durante el parseo y se encarga de las llamadas a las funciones que imprimen el resultado de esta Entrega.

En el archivo Func.py se define una clase llamada Func de la cual se crea una instancia para cada instrucción definida en una tarea (Task), esto para guardar toda la información importante que pueda tener una instrucción junto con su AST. Esta información es: Identificador de la instrucción, número de bloque asignado a esta instrucción y número de bloque donde fue definida esta instrucción.

En el archivo lexer.py se encuentra el analizador léxico de nuestro lenguaje. Obviaremos la explicación de él en este informe ya que este se encuentra en el informe de la Entrega 1.

En el archivo Print_functions.py se encuentran todas las funciones que sirven para hacer print de los resultados para esta entrega 2. Dos de estas funciones trabajan de manera recursiva para hacer más fácil el trabajo de imprimir todo con identación constante, en especial el AST de una tarea o instrucción definida.

En el archivo Tabla_simbolos.py se define la tabla de símbolos que se utilizara para los análisis de contexto. Esta tabla tendrá forma de pila en la cual empilaremos y desempilaremos en el tope las instrucciones definidas y las distintas variables definidas en un mundo por el usuario. Aparte de esto se hizo posible la búsqueda, usando el identificador, de estos símbolos en la tabla por medio de un ciclo que la recorre y regresa si existe y que tipo de variable es definida por este identificador. 

En el archivo Task.py se define una clase llamada Task de la cual se crea una instancia para cada tarea que se defina en el programa, esto para guardar toda la información importante que pueda tener la tarea junto con su AST. Esta información es: Identificador de la tarea, Identificador del mundo en el que se ejecuta la tarea y número de bloque asignado.

En el archivo willy.py se encuentra el programa principal que obtendrá los argumentos desde la consola del usuario y dará inicio a la ejecución del programa. Obviaremos la explicación de él en este informe ya que este se encuentra en el informe de la Entrega 1.

En el archivo World.py se define una clase llamada World de la cual se crea una instancia para cada mundo que se defina en el programa, esto para guardar toda la información importante que pueda tener el mundo junto con las variables que se definen en él. Esta información es: Identificador del mundo, lista de objetos con sus colores definidos en el mundo, lista de paredes que se encuentran en el mundo, capacidad de la bolsa de willy en el mundo, el grid del mundo representado como una matriz donde cada casilla contiene una instancia de la clase Casilla, dimensión del mundo, lista de objetos en la bolsa de willy, posición actual de willy en el mundo, lista de booleanos con sus valores definidos en el mundo, lista de objetivos definidos en el mundo y objetivo final del mundo. Cada método de esta clase devuelve True si la operación fue realizada con éxito o un string si ocurrió un error, donde el string da información acerca del error que ocurrió. Para guardar el objetivo final, el método definido para esto pide como argumento un árbol que define la expresión del objetivo final, este es recorrido usando DFS y generamos una lista ordenada de la expresión para así iterar por cada uno de los elementos y revisar si los elementos que la componen son objetivos previamente definidos o Booleanos definidos en el mundo. 

En el archivo wparser.py es donde se construyó el analizador sintáctico del lenguaje. Primero se empieza definiendo las precedencias de algunos Tokens para evitar ambiguedades: 
```bash
precedence = (
    ('left', 'TkOr'),
    ('left', 'TkAnd')
)
``` 
Donde el orden, empezando desde arriba, es de menor precedencia a mayor precedencia, el primer elemento de la tupla indica el sentido de la asociatividad y el segundo el Token. Mas adelante se definen unas funciones que nos ayuden a checkear la lista de tareas/mundos creados y la ultima es una funcion que regresa la linea y columna de un token, que sera utilizada principalmente para la impresión de errores. 

Luego pasamos a definir las distintas producciones o reglas utilizadas por nuestro analizador sintáctico. Primero empezamos por las reglas que definen la sintaxis de un mundo. Para cada mundo que se define en nuestro programa se genera una instancia de la clase World que luego que se termine de detectar todas las instrucciones del mundo se guardará esta instancia en una lista de mundos definidos. A medida que el analizador avance y reduzca la expresión, este tambien realizará una operación que agregue, en la instancia de la clase de ese mundo, lo que la instrucción analizada pida. Por ejemplo, si nos encontramos con la instruccion `World 5 5` el parser podrá analizarla como una instrucción de mundo y llamará al método de la clase World que se encargue de definir las dimensiones del mundo que estamos definiendo. Para los mundos no estamos generando un AST ya que, en vez de esto, estamos detectando estas instrucciones y guardando esa información directamente en la instancia del mundo definido.

Luego definimos las reglas que definen la sintaxis de una tarea o Task. Para cada tarea que se define en nuestro programa se genera una instancia de la clase Task, donde,una vez que se termine de detectar las instrucciones que componen la tarea, este obtendrá el AST de la tarea y la instancia de guardará en una lista de tareas definidas. A diferencia de los mundos, para las tareas si guardaremos el AST en vez de tomar accion directamente sobre el mundo o la instancia de la clase Task. En las tareas podemos definir instrucciones compuestas, las cuales no guardamos en el AST de la tarea sino que, una vez detectadas las instrucciones que la componen, guardamos su AST en una instancia de la clase Func y esta a su vez es guardada en la Tabla de Simbolos (Para poder llevar a cabo el análisis de contexto) y en una lista de instrucciones compuestas definidas en el programa.

Para diferenciar las condiciones de la instrucción `Final Goal is ...` y las de las instrucciones `if ...`, `if ... else ...` y `while ...` definimos dos reglas diferentes para el analizador sintáctico. Esto se hizo ya que las condiciones de la instruccion de mundo son diferentes a las de las instrucciones de tarea. Las condiciones del objetivo final solo aceptan identificadores de objetivos o booleanos previamente definidos, mientras que las condiciones de los if y while aceptan identificadores de booleanos definidos en el mundo sobre el cual la tarea se ejecuta y booleanos literales.

Para la impresiond de errores se definió una función de ply yacc que detecta los errores sintácticos, imprime donde ocurrió y aborta la ejecución del programa. Mientras que para los errores de contextos, estos se imprimen mientras se encuentran pero asignan True a un booleano que indica si durante la ejecución se encontro un error de contexto, para asi imprimir todos los errores de este tipo y al final del análisis abortar el programa.

La tabla de simbolos fue implementada como una clase que se instancia una sola vez en el programa. En esta se empilan y desempilan simbolos mediante el analisis sintáctico de los mundos y tareas. Luego de definir una tarea, esta tabla se vacia por completo y se deja limpia para las futuras tareas que se piensen definir.

Para ejecutar nuestro programa se debe hacer lo siguiente:

```bash
make
willy [argumento]
```

vale acotar que debe existir el directorio ${HOME}/bin y que willy no debe existir en esa carpeta al hacer make.