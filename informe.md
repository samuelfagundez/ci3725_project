## Informe 3

#### Etapa Ejecucion: Creamos un entorno grafico para visualizar los estados de willy, el cual se encuentra en interfaz.py, se utilizo la libreraria PyQt5. En el archivo execute.py se encuentra el manejador de instrucciones, que primero decide la modalidad de ejecucion y que luego interpreta la instruccion para realizar lo que corresponda con Willy. Las tasks requeridas en el proyecto se encuentran en programas_willy.txt. Se modifico World.py para agregar las instrucciones atomicas que manipulan a Willy durante una ejecucion.

#### Ademas se solucionaron correcciones del preparador como utilizar el metodo keys() de python3 para obtener los ids de los elementos en un diccionario.

##### Los diferentes archivos añadidos y modificados fueron:

###### - execute.py

###### - Interfaz.py

###### - programas_willy.txt

###### - World.py

###### La interfaz se encuentra implementada en Interfaz.py, cuenta solo con los elementos necesarios, un tablero para representar las casillas, contiene un boton next para ejecutar el siguiente paso, cancelar el programa y una lista de los elementos para el basket del willy y para las casillas. Cada actualizacion del estado de willy genera un reboot en el programa y se inicia con el nuevo estado, esto porque hacer una interfaz estable requeria trabajo que se apartaba del objetivo real del proyecto.

###### En World.py se encuentra el generador del mundo y todos los metodos requeridos para emplear modificaciones en un mundo y en willy. Tambien se añadieron las operaciones atomicas de Willy que lo manipulan en las ordenes con la cual se interactua con willy, Move, Turn Left, Turn Right, Pick y Drop. Se hizo una modificacion en el metodo isWallInCell de la entrega anterior para añadir la direccion en la que willy observa o None si es para la casilla en si. Ademas ahora las llaves de los diccionarios se obtienen con el metodo keys() de python.

###### En execute.py se controla la ejecucion del programa. waitModalidad es una funcion que se encarga de controlar si la ejecucion de nuestro programa es manual o automatico. buildGUI es quien genera la ventana de ejecucion con el nuevo mundo. execute es una funcion que permite obtener el arbol de tareas de una task, ejecturla y luego verificar si termino con exito o en fracaso. success_condition es una funcion que sirve para verificar si al final culminar la tarea se satisface o no la condicion de exito. condition_recursive es quien evalua y mantiene el orden y ejecuta las instrucciones if y while. execute_recursive recorre el AST y ejecuta instruccion por instruccion, dentro de esta funcion se encuentra la llamada a waitModalidad para controlar si la llamada es manual o automatica.

###### En programas_willy.txt se encuentran algunos ejemplos de tareas que puede realizar willy.

Para ejecutar nuestro programa se debe hacer lo siguiente:

```bash
make
willy [argumento]
```

El argumento en esta etapa consiste en el siguiente: willy <archivo_de_texto_con_las_task> <nombre_task> -m/-a para manual o automatico

vale acotar que debe existir el directorio /\${HOME}/bin y willy no debe existir en esa carpeta al hacer make.
