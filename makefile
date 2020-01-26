all:
	pip3 install pyinstaller
	pyinstaller --onefile willy.py
	sudo cp dist/willy /bin