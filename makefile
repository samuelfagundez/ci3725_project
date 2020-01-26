all:
	python3 -m pip install pyinstaller
	pyinstaller --onefile main.py