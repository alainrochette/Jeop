from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtMultimedia as M
# from PyQt5 import QtGui, QtCore
# from Pic import Pic
import pandas as pd
# + = []
class LoadMenu(QMainWindow):
	def __init__(self, main):
		super().__init__()
		# super().setStyleSheet("background-color: black")

		super().setStyleSheet("QMainWindow {background-image:url(\"assets/jeopBack.png\")}")
		self.main = main
		self.games = pd.read_excel('Games.xlsx',sheet_name=None)

		self.gameNames = self.games.keys()
		# songapp=QCoreApplication([""])

		# song = QSound("jeopTheme.mp3")
		# song.play()
		# player.stateChanged.connect( songapp.quit )
		# self.players = []
		# main.player_names = []

		goBackBox = QVBoxLayout()
		goBackBox.setAlignment(Qt.AlignLeft)
		backb = QPushButton("Back")
		backb.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;'
									'border: 1px solid #FFFFFF; background-color: transparent; color:white;border-radius: 15px;}'
									'QPushButton:hover { background-color: gray;}'
									'height: 68px;width: 48px; align:center')
		backb.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		backb.setMinimumSize(150,44)

		# play.clicked.connect(lambda: self.start_game(self.games[g]))
		backb.clicked.connect(lambda: self.main.handle_menustart())
		goBackBox.addWidget(backb)

		title = QVBoxLayout()
		# title.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
		# title.setAlignment(Qt.AlignTop)
		titleLabel = QLabel()
		titleLabel.setStyleSheet("QLabel {background-image:url(\"assets/jeopLogo.png\")}")
		titleLabel.setMinimumSize(863,227)

		title.addWidget(titleLabel)
		title.setAlignment(Qt.AlignCenter)

		allgamesBox = QHBoxLayout()
		allgamesBox.setSpacing(2)


		count = 1
		for game in reversed(list(self.gameNames)):
			if count % 3 == 1:
				columnGamesBox = QVBoxLayout()
				columnGamesBox.setAlignment(Qt.AlignCenter)
				columnGamesBox.setSpacing(20)
			play = QPushButton(game)
			play.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 30pt;font-weight: bold;'
										'border: 0px solid #FFFFFF; background-color: purple; color:white;border-radius: 15px;}'
										'QPushButton:hover { background-color: #b01adb;}'
										'height: 68px;width: 48px; align:center')
			play.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
			play.setMinimumSize(300,88)

			# play.clicked.connect(lambda: self.start_game(self.games[g]))
			play.clicked.connect(lambda: self.start_game(game))
			columnGamesBox.addWidget(play)
			if count % 3 == 0:
				allgamesBox.addLayout(columnGamesBox)
			count += 1
		if count+1 % 3 != 0: allgamesBox.addLayout(columnGamesBox)
		#
		# playreal = QPushButton("Play Real")
		# playreal.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 40pt;font-weight: bold;'
		# 							'border: 0px solid #FFFFFF; background-color: purple; color:white;}'
		# 							'QPushButton:hover { background-color: #b01adb;}'
		# 							'height: 68px;width: 48px; align:center')
		# playreal.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		# playreal.setMinimumSize(300,88)
		# # playreal.clicked.connect(lambda: self.start_game(True))
		#
		# playButtonBox.setAlignment(Qt.AlignCenter)
		# # playButtonBox.setAlignment(Qt.AlignTop)
		# playButtonBox.addWidget(play)
		# playButtonBox.addWidget(playreal)
		#
		# # playBox.addLayout(contestantsBox)
		# playBox.addLayout(playersBox)
		# playBox.addLayout(playButtonBox)
		# playBox.setSpacing(15)
		#
		#
		layout = QVBoxLayout()
		layout.setSpacing(0)
		layout.addLayout(goBackBox)
		layout.addLayout(title)
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.addLayout(allgamesBox)
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

	def start_game(self, game):
		# for p in self.playersInput:
		# 	if p.text() == "":
		# 		return

		# self.main.player_names = [p.text() for p in self.playersInput]
		self.main.handle_gamestart(game)
