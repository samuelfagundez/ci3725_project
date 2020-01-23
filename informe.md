### Informe 1

##### Etapa Lexer: Construimos el Lexer utilizando Python, se utilizan tres archivos relevantes files.py, lexer.py y main.py.

###### En el lexer.py está todo lo relacionado con el lexer, la definición de todos los tokens y palabras reservadas, y las funciones de reconocimiento a través de expresiones regulares de dichos tokens. Cada funcione se define con el nombre t_{TOKEN} que es necesario para el reconocimiento de los tokens. Además hay una funcion de reconocimiento de errores llamada t_error.

Explicar un ejemplo de como se mapea un regex a un token

###### En el files.py se encuentra una función que se encarga de abrir el archivo a procesar, lo abre, lo lee, guardamos nuestros tokens en una estructura de datos de tipo Lista y luego imprimimos todos los tokens respetando la forma propuesta por el preparador.

###### La forma de impresión de los tokens en la salida es la siguiente:
###### Para los TkId es: TkId("value", linea=x, columna=y)
###### Para los TkNum es: TkNum(num, linea=x, columna=y)
###### Para los Tk{PalabraReservada} es: Tk{PalabraReservada}(linea=x, columna=y)

###### En main.py se efectuan las llamadas al programa.