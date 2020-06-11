from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtMultimedia as M
from MenuButton import MenuButton

N_PLAYERS = 4
class Menu(QMainWindow):
	def __init__(self, main):
		super().__init__()
		super().setStyleSheet("QMainWindow {background-image:url(\"assets/jeopBack.png\")}")
		self.main = main

		title = QVBoxLayout()
		titleLabel = QLabel()
		titleLabel.setStyleSheet("QLabel {background-image:url(\"assets/jeopLogo.png\")}")
		titleLabel.setMinimumSize(863,227)

		title.addWidget(titleLabel)
		title.setAlignment(Qt.AlignCenter)

		playersBox = QVBoxLayout()

		self.playersInput = [QLineEdit(self) for i in range(N_PLAYERS)]
		pcount = 1
		for p in self.playersInput:
			p.setMaximumSize(400,max(40,140 - 24*len(self.playersInput)))
			fsize = str(50 - 5*(len(self.playersInput)-2))
			p.setStyleSheet('QLineEdit {font-family: Arial;font-style: normal;font-size: '+fsize+'pt;font-weight: bold;'
										'border: 1px solid #FFFFFF; background-color: transparent; color:#b01adb;'
										'border-radius: 10px;}'
										'height: 48px;width: 18px; align:center;')
			p.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
			p.setAlignment(QtCore.Qt.AlignCenter)
			p.setMinimumSize(400,max(40,140 - 24*len(self.playersInput)))
			f = p.font()
			f.setPointSize(35-5*(len(self.playersInput)-2))
			p.setFont(f)
			p.setPlaceholderText("Player " + str(pcount));
			pcount += 1

		list(map(lambda p: playersBox.addWidget(p), self.playersInput))
		playersBox.setAlignment(Qt.AlignCenter)




		playBox = QVBoxLayout()

		playButtonBox = QHBoxLayout()
		create = MenuButton(self,"Create","normal").button
		create.clicked.connect(lambda: self.start_game("Create"))
		play =  MenuButton(self,"Play Custom","normal").button
		play.clicked.connect(lambda: self.start_game("Custom"))
		playreal = MenuButton(self,"Play Real","normal").button
		playreal.clicked.connect(lambda: self.start_game("Real"))

		playButtonBox.setAlignment(Qt.AlignCenter)
		playButtonBox.addWidget(create)
		playButtonBox.addWidget(play)
		playButtonBox.addWidget(playreal)

		playBox.addLayout(playersBox)
		playBox.addLayout(playButtonBox)
		playBox.setSpacing(15)


		layout = QVBoxLayout()
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.setSpacing(0)
		layout.addLayout(title)
		layout.addLayout(playBox)
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))


		self.mainWidget = QWidget()
		self.mainWidget.setLayout(layout)
		self.setCentralWidget(self.mainWidget)
		self.resize(1500,1200)
		self.show()

	def start_game(self, type):
		# self.playersInput = ["Player " + str(i+1)  if self.playersInput[i].text() == "" else self.playersInput[i].text() for i in range(len(self.playersInput))]
		self.main.player_names =  [self.playersInput[i].text() for i in range(len(self.playersInput)) if self.playersInput[i].text() != "" ]
		self.main.handle_loadmenustart(type)
