all:
	pip3 install pyinstaller
	pyinstaller --onefile willy.py
	cp dist/willy  ${HOME}/bin
	rm -r dist/
	rm -r build/