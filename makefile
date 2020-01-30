all:
	#instalar pyinstaller
	pip3 install pyinstaller
	#crear ejecutable
	pyinstaller --onefile willy.py
	#remover willy viejo si existe
	rm -f ${HOME}/bin/willy
	#copiar nuevo willy
	cp dist/willy  ${HOME}/bin
	#remover archivos sobrantes
	rm -r dist/
	rm -r build/