from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtMultimedia as M
# from PyQt5 import QtGui, QtCore
# from Pic import Pic
# + = []
class Menu(QMainWindow):
	def __init__(self, main):
		super().__init__()
		# super().setStyleSheet("background-color: black")

		super().setStyleSheet("QMainWindow {background-image:url(\"assets/jeopBack.png\")}")
		self.main = main

		# songapp=QCoreApplication([""])

		# song = QSound("jeopTheme.mp3")
		# song.play()
		# player.stateChanged.connect( songapp.quit )
		# self.players = []
		# main.player_names = []


		title = QVBoxLayout()
		# title.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
		# title.setAlignment(Qt.AlignTop)
		titleLabel = QLabel()
		titleLabel.setStyleSheet("QLabel {background-image:url(\"assets/jeopLogo.png\")}")
		titleLabel.setMinimumSize(863,227)

		title.addWidget(titleLabel)
		title.setAlignment(Qt.AlignCenter)

		playersBox = QVBoxLayout()
		# contestantsBox = QVBoxLayout()
		# contestants = QLabel("Today's Contestants:")
		# contestants.setStyleSheet('QLabel {font-family: Arial;font-style: normal;font-size: 20pt;font-weight: regular;'
		# 							'border: 0px solid #FFFFFF; background-color: transparent; color:white;}'
		# 							'QPushButton:hover { background-color: #b01adb;}'
		# 							'height: 18px;width: 48px; align:center')
		# contestants.setAlignment(QtCore.Qt.AlignCenter)
		# contestants.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		# contestants.setMaximumSize(1600,40)
		# contestantsBox.addWidget(contestants)


		self.playersInput = [QLineEdit(self) for i in range(3)]
		pcount = 1
		for p in self.playersInput:
			p.setMaximumSize(400,40)
			p.setStyleSheet('QLineEdit {font-family: Arial;font-style: normal;font-size: 50pt;font-weight: bold;'
										'border: 1px solid #FFFFFF; background-color: transparent; color:#b01adb;'
										'border-radius: 10px;}'
										'height: 48px;width: 18px; align:center;')
			p.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
			p.setAlignment(QtCore.Qt.AlignCenter)
			p.setMinimumSize(400,60)
			# p.SetStyleSheet("font-family: Arial;font: 20px;font-weight: bold;")
			f = p.font()
			f.setPointSize(35)
			p.setFont(f)
			p.setPlaceholderText("Player " + str(pcount));
			pcount += 1

		list(map(lambda p: playersBox.addWidget(p), self.playersInput))
		playersBox.setAlignment(Qt.AlignCenter)




		playBox = QVBoxLayout()

		playButtonBox = QHBoxLayout()
		# super().setStyleSheet("background-color: transparent;")
		play = QPushButton("Play Custom")
		play.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 40pt;font-weight: bold;'
									'border: 0px solid #FFFFFF; background-color: purple; color:white;border-radius: 15px;}'
									'QPushButton:hover { background-color: #b01adb;}'
									'height: 68px;width: 48px; align:center')
		play.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		play.setMinimumSize(300,88)
		play.clicked.connect(lambda: self.start_game(False))

		playreal = QPushButton("Play Real")
		playreal.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 40pt;font-weight: bold;'
									'border: 0px solid #FFFFFF; background-color: purple; color:white;border-radius: 15px;}'
									'QPushButton:hover { background-color: #b01adb;}'
									'height: 68px;width: 48px; align:center')
		playreal.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		playreal.setMinimumSize(300,88)
		# playreal.clicked.connect(lambda: self.start_game(True))

		playButtonBox.setAlignment(Qt.AlignCenter)
		# playButtonBox.setAlignment(Qt.AlignTop)
		playButtonBox.addWidget(play)
		playButtonBox.addWidget(playreal)

		# playBox.addLayout(contestantsBox)
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
		# layout.addLayout(playersBox)
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


		# playBox = QVBoxLayout()
		# playBox.addWidget(self.own_dice)
		# playBox.addLayout(diff)
		# self.setLayout(playBox)
		# self.resize(500, 500)

	def start_game(self, real):
		for p in self.playersInput:
			if p.text() == "":
				return

		self.main.player_names = [p.text() for p in self.playersInput]
		# self.main.handle_gamestart(real)
		self.main.handle_loadmenustart()
		# self.main.handle_gamestart(real)
