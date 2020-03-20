from PyQt5.QtGui import QIcon, QPalette, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import *
from copy import deepcopy
import sys

# Crea el Grid del mundo
class grid(QTableWidget):
    def __init__(self, place, mundo):
        super().__init__(place)
        dimX, dimY = mundo.getWorldDim()
        self.setColumnCount(dimX) #Columnas
        self.setRowCount(dimY)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch) #Ajuste de tamaño
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setStyleSheet("background-color:  Silver")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumSize(870, 870)
        self.setMinimumSize(870, 870)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.update(mundo)


    # Hace update al grid del mundo
    def update(self, mundo):

        # Coloca las paredes del mundo
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                if mundo.isWallInCell(j+1, self.rowCount()-i, None):
                    self.setItem(i, j, QTableWidgetItem())
                    self.item(i, j).setBackground(QColor(0, 0, 0))
                else:
                    self.setCellWidget(i, j, QPushButton())
                    # Si la casilla tiene un objeto, la pintamos de color diferente
                    if len(mundo.world[j][self.rowCount()-i-1].getAllObjetos()) > 0:
                        self.cellWidget(i, j).setStyleSheet("background-color: rgb(200,200,200);")
                    else:
                        self.cellWidget(i, j).setStyleSheet("background-color: rgb(255,255,255);")
                    # Obtenemos la posicion de willy y lo reflejamos en el mundo
                    pos = mundo.getWillyPos()
                    if self.rowCount()-i == pos[1] and (j+1) == pos[0]:
                        self.cellWidget(i, j).setText("   W\n(" + pos[2] + ")")


# Crea la ventana principal del programa
class window(QMainWindow):
    def __init__(self, sleep, mundo):
        super().__init__()
        self.setWindowTitle(mundo.getId())
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.setFixedSize(1300, 900)

        # Fonts
        self.title = QFont("Serif", 17)
        self.objectFont = QFont("Serif", 14)

        # Si el grid se actualiza en "sleep" cantidad de segundos
        if sleep != 21474:
            timer = QTimer(self)
            timer.setInterval(sleep * 1000)
            timer.timeout.connect(self.close)
            timer.start()
        # Si el grid no se actualiza automaticamente
        else:
            # Boton para obtener el siguiente movimiento de willy
            self.next_move = QPushButton("Next Move", self)
            self.next_move.setFixedSize(100, 30)
            self.next_move.move(0, 0)
            self.next_move.clicked.connect(lambda: self.close())
        
        # Boton para cancelar la ejecucion del programa
        self.cancel = QPushButton("Cancel", self)
        self.cancel.setFixedSize(100, 30)
        self.cancel.move(100, 0)
        self.cancel.clicked.connect(lambda: sys.exit())

        # Frame de objetos en bolsa de willy
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFixedWidth(370)
        self.frame.setFixedHeight(435)
        self.frame.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: white;\n"
        "}")
        self.frame.move(900, 30)

        # Titulo de frame
        self.info_frame = QFrame(self.frame)
        self.info_frame.setFrameShape(QFrame.NoFrame)
        self.info_frame.setFrameShadow(QFrame.Sunken)
        self.info_frame.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.info_frame.setFixedWidth(350)
        self.info_frame.setFixedHeight(40)
        self.info_frame.move(10, 10)
        self.label = QLabel("Bolsa Willy", self.info_frame)
        self.label.move(113, 5)
        self.label.setFont(self.title)

        # Contenido de la bolsa
        bolsa = mundo.getBasket()
        i = 0
        for obj in bolsa:
            color = mundo.searchColorOfObject(obj)
            self.color = QLabel("   ", self.frame)
            self.color.move(10, 66 + i*(30))
            self.color.setStyleSheet("QLabel \n{\nbackground-color: " + color + "\n; border: 1px solid black;}")
            self.object = QLabel(obj +": "+ str(bolsa[obj]), self.frame)
            self.object.move(40, 60 + i*(30))
            self.object.setFont(self.objectFont)
            i += 1

        # Frame de Objetos en casilla
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFixedWidth(370)
        self.frame.setFixedHeight(435)
        self.frame.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: white;\n"
        "}")
        self.frame.move(900, 465)

        # Titulo de frame
        self.info_frame = QFrame(self.frame)
        self.info_frame.setFrameShape(QFrame.NoFrame)
        self.info_frame.setFrameShadow(QFrame.Sunken)
        self.info_frame.setStyleSheet("QFrame \n"
        "{\n"
        "background-color: #79B9E0;\nborder: 1px;\n border-radius: 3px;\n"
        "}")
        self.info_frame.setFixedWidth(350)
        self.info_frame.setFixedHeight(40)
        self.info_frame.move(10, 10)
        self.label = QLabel("Objetos en Casilla", self.info_frame)
        self.label.move(65, 5)
        self.label.setFont(self.title)

        # Grid del mundo
        self.grid = grid(self, mundo)
        self.grid.move(0, 30)

        # Aqui se guardaran los objetos de casillas que estan siendo mostrados al momento
        self.objetos_anteriores = []
        # Muestra los objetos de una casilla
        for i in range(self.grid.rowCount()):
            for j in range(self.grid.columnCount()):
                if not mundo.isWallInCell(j+1, self.grid.rowCount()-i, None):
                    # Para cada boton, si se presiona, muestra los objetos que tiene en el frame Objetos en Casilla
                    self.grid.cellWidget(i, j).clicked.connect(lambda checked, objetos=self.ObjectsInCell(mundo, j+1, self.grid.rowCount()-i): self.showObjects(objetos))

    # Muestra los objetos en la casilla
    def showObjects(self, objetos):
        # Esconde los objetos actualmente mostrados
        for obj in self.objetos_anteriores:
            obj[0].hide()
            obj[1].hide()
        # Muestra los objetos de la casilla que se desea mostrar
        for obj in objetos:
            obj[0].show()
            obj[1].show()
        self.objetos_anteriores = objetos

    # Calcula todos los objetos de la casilla
    def ObjectsInCell(self, mundo, columna, fila):

        # Contenido de la casilla
        casilla = mundo.world[columna-1][fila-1].getAllObjetos()
        i = 0
        objects = []
        for obj in casilla:
            color = mundo.searchColorOfObject(obj)
            self.color = QLabel("   ", self.frame)
            self.color.move(10, 66 + i*(30))
            self.color.setStyleSheet("QLabel \n{\nbackground-color: " + color + "\n; border: 1px solid black;}")
            self.object = QLabel(obj +": "+ str(casilla[obj]), self.frame)
            self.object.move(40, 60 + i*(30))
            self.object.setFont(self.objectFont)
            self.color.hide()
            self.object.hide()
            objects.append([self.color, self.object])
            i += 1

        return objects