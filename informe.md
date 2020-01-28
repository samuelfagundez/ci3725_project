### Informe 1

##### Etapa Lexer: Construimos el Lexer utilizando Python, se utilizan tres archivos relevantes files.py, lexer.py y main.py.

###### En el lexer.py está todo lo relacionado con el lexer, la definición de todos los tokens, palabras reservadas y las funciones de reconocimiento a través de expresiones regulares de dichos tokens. Cada funcione se define con el nombre t_{TOKEN} que es necesario para el reconocimiento de los tokens. Además hay una funcion de reconocimiento de errores llamada t_error, encargada de imprimir cuando hay una inconsistencia (caracter ilegal) como por ejemplo los "-".

###### Cada vez que se llama el lexer para reconocer una expresión el programa corre de manera síncrona, por lo cual se va ejecutando cada función de arriba hasta abajo, en el momento en el que coincide alguna expresión se devuelve dicho token, el cual es procesado por files.py.

###### Por ejemplo, la llamada de la función t_TkId mapea el siguiente regex [a-zA-Z_][a-zA-Z_0-9\-]* el cual es equivalente a todas las palabras no vacías que contengan los caracteres almacenados dentro de [ ], además contiene una validación en el cual si se cumple que dicho string contiene el caracter "-" significa que este ID no es soportado por el contrario si es válido pues continúa y devuelve el token para que lo procese files.py.

###### En el files.py se encuentra una función que se encarga de abrir el archivo a procesar (argumento), lo abre, lo lee, guardamos nuestros tokens en una estructura de datos de tipo Lista y luego imprimimos todos los tokens respetando la forma propuesta por el preparador.

###### La estructura de datos que utilizamos para almacenar los tokens es una lista de listas, donde cada posición de la primera lista representa una lista con los tokens de la i-esima linea, si el length de alguno de los elementos de la primera lista es 0 significa que en esa linea correspondía a comentarios o espacio en blanco.

###### Es importante aclarar que en caso de contener errores nuestro programa, solo se imprimen los errores o caracteres ilegales, en caso de éxito se imprimen los tokens.

###### La forma de impresión de los tokens en la salida es la siguiente:
###### Para los TkId es: TkId("value", linea=x, columna=y)
###### Para los TkNum es: TkNum(num, linea=x, columna=y)
###### Para los Tk{PalabraReservada} es: Tk{PalabraReservada}(linea=x, columna=y)

###### En main.py se efectuan las llamadas al programa.

##### Para ejecutar nuestro programa se debe hacer lo siguiente:
###### make
###### willy <argumento || vacío>
###### vale acotar que debe existir el directorio ${HOME}/bin y que willy no debe existir en esa carpeta al hacer make.