all:
	#instalar pyinstaller
	pip install pyinstaller
	#instalar la ultima version de pyqt5
	pip install pyqt5
	#instalar ply
	pip install ply
	#crear ejecutable
	pyinstaller --onefile willy.py
	#remover willy viejo si existe
	rm -f ${HOME}/bin/willy
	#copiar nuevo willy
	cp dist/willy  ${HOME}/bin
	#remover archivos sobrantes
	rm -r dist/
	rm -r build/