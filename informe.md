## Informe 3

#### Etapa Ejecucion: Creamos un entorno grafico para visualizar los estados de willy, el cual se encuentra en interfaz.py, se utilizo la libreraria PyQt5. En el archivo execute.py se encuentra el manejador de instrucciones, que primero decide la modalidad de ejecucion y que luego interpreta la instruccion para realizar lo que corresponda con Willy. Las tasks requeridas en el proyecto se encuentran en programas_willy.txt. Se modifico World.py para agregar las instrucciones atomicas que manipulan a Willy durante una ejecucion.

#### Ademas se solucionaron correcciones del preparador como utilizar el metodo keys() de python3 para obtener los ids de los elementos en un diccionario.

##### Los diferentes archivos a;adidos y modificados fueron:

###### - execute.py

###### - Interfaz.py

###### - programas_willy.txt

###### - World.py

###### La interfaz esta implementada con los elementos necesarios, contiene un boton next para ejecutar el siguiente paso, cancelar el programa y una lista de los elementos para el basket del willy y para las casillas. Cada actualizacion del estado de willy genera un reboot en el programa y se inicia con el nuevo estado, esto porque hacer una interfaz estable requeria trabajo que se apartaba del objetivo real del proyecto.

###### En World.py se hizo una modificacion en el metodo isWallInCell para a;adir la direccion en la que willy observa o None si es para la casilla en si. Ademas ahora las llaves de los diccionarios se obtienen con el metodo keys() de python. Ademas se a;adieron las operaciones atomicas de Willy que lo manipulan en las ordenes con la cual se interactua con willy, Move, Turn Left, Turn Right, Pick y Drop.

###### En execute.py controla la ejecucion del programa, waitModalidad es una funcion que se encarga de controlar si la ejecucion de nuestro programa es manual o automatico. buildGUI es quien genera la ventana de ejecucion con el nuevo mundo. executeRecursive .

###### En programas_willy.txt se encuentran algunos ejemplos de tareas que puede realizar willy.

Para ejecutar nuestro programa se debe hacer lo siguiente:

```bash
make
willy [argumento]
```

luego willy programas_willy.txt task1(task2, task3, task4....) -m/-a para manual o automatico

vale acotar que debe existir el directorio \${HOME}/bin y que willy no debe existir en esa carpeta al hacer make.
