from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtMultimedia as M
# from PyQt5 import QtGui, QtCore
# from Pic import Pic
# + = []
class DoubMenu(QMainWindow):
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
		titleLabel.setStyleSheet("QLabel {background-image:url(\"assets/doubJeopLogo.png\")}")
		titleLabel.setMinimumSize(835,405)

		title.addWidget(titleLabel)
		title.setAlignment(Qt.AlignCenter)



		playBox = QVBoxLayout()

		playButtonBox = QVBoxLayout()
		# super().setStyleSheet("background-color: transparent;")
		play = QPushButton("Play")
		play.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 40pt;font-weight: bold;'
									'border: 0px solid #FFFFFF; background-color: purple; color:white;border-radius: 15px;}'
                                    'QPushButton:hover { background-color: #b01adb;}'
									'height: 68px;width: 48px; align:center')
		play.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		play.setMinimumSize(300,50)
		play.clicked.connect(self.start_game)
		playButtonBox.setAlignment(Qt.AlignCenter)
		# playButtonBox.setAlignment(Qt.AlignTop)
		playButtonBox.addWidget(play)

		playBox.addLayout(playButtonBox)


		playersBox = QHBoxLayout()

		pcount = 1
		for p in self.main.players:
			playerBox = QVBoxLayout()
			score = QLabel(str(p.score))


			# p.setMaximumSize(400,40)
			score.setStyleSheet('QLabel {font-family: Arial;font-style: normal;font-size: 50pt;font-weight: bold;'
										'border: 3px solid #FFFFFF; background-color: #000292; color:white;}'
										'height: 418px;width: 48px; align:center')
			score.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
			score.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

			name = QLabel(str(p.name))

			name.setStyleSheet('QLabel {font-family: Arial;font-style: normal;font-size: 40pt;font-weight: thin;'
									'border: 0px solid #FFFFFF; background-color: #000292; color:white;}'
									'height: 418px;width: 48px; align:center')


			name.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
			name.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
			playerBox.addWidget(score)
			playerBox.addWidget(name)
			playerBox.setSpacing(0)
			playerBox.setAlignment(Qt.AlignCenter)
			playersBox.addLayout(playerBox)


		playersBox.setAlignment(Qt.AlignCenter)






		layout = QVBoxLayout()
		layout.setSpacing(80)
		layout.addLayout(title)
		layout.addLayout(playersBox)
		layout.addLayout(playBox)

		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		layout.addWidget(QLabel(""))
		# self.layout.setAlignment(Qt.AlignHCenter)

		# self.own_dice = QCheckBox("I have my own dice, tyvm")
		#
		# self.easy= QPushButton("Easy")
		# self.medium = QPushButton("Medium")
		# self.hard = QPushButton("Hard")

		#
		# self.medium.setEnabled(False)
		# self.hard.setEnabled(False)
		#
		# diff = QHBoxLayout()
		# diff.addWidget(self.easy)
		# diff.addWidget(self.medium)
		# diff.addWidget(self.hard)


		# self.easy.clicked.connect(self.start_game)
		# self.medium.clicked.connect(self.start_game)

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

	def start_game(self, diff):
		# self.main.player_names = [p.text() for p in self.playersInput]
		self.main.handle_doublejeopardy()
