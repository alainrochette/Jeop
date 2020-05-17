from random import choice, randint
import PyQt5
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import *

# + = []
greenTransition = ["#03aa36","#03aa6e","#03aaa3","#037faa","#0352aa","#000292"]
redTransition = ["#e00022","#cc0060","#bd00a0","#9001b2","#5900a3","#000292"]

greenTransitionEdit = ["#14d600","#70e600","#70e600","#ffaf6b","#ffaf6b","salmon"]
redTransitionEdit = ["#b2242a","#cf262d","#dd3138","#e4444a","#e75f64","salmon"]

class Player:
	def __init__(self, game,name):
		self.game = game
		self.score = 0
		self.name = name
		self.b_score = self.bPlayerScore()
		self.b_name = self.bPlayerName()
		self.b_add = self.bAdd()
		self.b_rem = self.bRem()
		self.edit = False
		self.timer = None
		self.colorindex= 0


	def changeColor(self, add):

		if self.colorindex < len(greenTransition):
			t = greenTransition if add else redTransition
			t = greenTransitionEdit if add and self.edit else t
			t = redTransitionEdit if not add and self.edit else t
			self.b_score.setStyleSheet('QLineEdit {font-family: Arial;font-style: normal;font-size: 50pt;font-weight: bold;'
										'border: 1px solid #FFFFFF; background-color:'+str(t[self.colorindex])+'; color:white;}'
										'height: 418px;width: 48px; align:center')
			self.colorindex += 1
		else:
			self.colorindex = 0
			self.timer  = None

	def roll(self):
		dice = [str(randint(1, 6)) for _ in range(self.count)]
		self.dice = "".join(dice)

	def add_dice(self):
		self.count = min(5, self.count + 1)

	def remove_dice(self):
		self.count -= 1

	def remPoints(self, points):
		self.score -= points
		self.b_score.setText(str(self.score))
		self.timer = QTimer()
		self.timer.timeout.connect(lambda: self.changeColor(False))
		self.timer.start(50)

	def addPoints(self, points):
		self.score += points
		self.b_score.setText(str(self.score))
		self.timer = QTimer()
		self.timer.timeout.connect(lambda: self.changeColor(True))
		self.timer.start(50)


	def bPlayerScore(self):
		# p = QPushButton("0")
		p = QLineEdit()
		p.setText("0")
		p.setStyleSheet('QLineEdit {font-family: Arial;font-style: normal;font-size: 50pt;font-weight: bold;'
									'border: 1px solid #FFFFFF; background-color: #000292; color:white;}'
									'height: 418px;width: 48px; align:center')
		p.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
		# p.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		p.setReadOnly(True)
		p.setAlignment(QtCore.Qt.AlignCenter)
		p.setValidator(QIntValidator(-999999,99999, None))
		p.returnPressed.connect(lambda: self.stopEdit())
		p.textEdited.connect(lambda: self.newScore())
		return p

	def bPlayerName(self):
		p = QPushButton(self.name)
		p.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 40pt;font-weight: thin;'
								'border: 0px solid #FFFFFF; background-color: #000292; color:white;}'
								'height: 418px;width: 48px; align:center')
		p.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Preferred)
		# p.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		p.clicked.connect(lambda: self.toggleEdit())
		return p

	def bAdd(self):
		b = QPushButton("+")
		b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 30pt;font-weight: bold;'
								'border: 1px solid green; background-color: black; color:green;}'
								'QPushButton:hover { background-color: lightgreen;}'
								'height: 28px;width: 38px;')
		b.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		b.setMinimumWidth(30)
		b.clicked.connect(lambda: self.game.playerAdd(self))

		return b

	def bRem(self):
		b = QPushButton("-")
		b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 30pt;font-weight: bold;'
								'border: 1px solid red; background-color: black; color:red;}'
								'QPushButton:hover { background-color: salmon;}'
								'height: 28px;width: 38px;')
		b.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		b.setMinimumWidth(30)
		b.clicked.connect(lambda: self.game.playerRem(self))

		return b

	def newScore(self):
		try:
			self.score = int(self.b_score.text())
		except ValueError:
			pass

	def toggleEdit(self):
		if self.edit:
			self.stopEdit()
		else:
			self.edit = True
			self.b_score.setReadOnly(False)
			self.b_score.setStyleSheet('QLineEdit {font-family: Arial;font-style: normal;font-size: 50pt;font-weight: bold;'
											'border: 1px solid #FFFFFF; background-color:salmon; color:white;}'
											'height: 418px;width: 48px; align:center')
			self.b_score.setFocus()
			self.b_score.end(False)

	def stopEdit(self):
		self.score = int(self.b_score.text())
		self.edit = False
		# self.b_score.cursorPositionAt(0)
		self.b_score.setReadOnly(True)
		self.b_score.setStyleSheet('QLineEdit {font-family: Arial;font-style: normal;font-size: 50pt;font-weight: bold;'
										'border: 1px solid #FFFFFF; background-color:#000292; color:white;}'
										'height: 418px;width: 48px; align:center')
		# if self.edit:
		#
		# 	self.b_score.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 50pt;font-weight: bold;'
		# 								'border: 0px solid #FFFFFF; background-color:#000292; color:white;}'
		# 								'height: 418px;width: 48px; align:center')
		# 	self.edit=False
		# else:
		#
		# 	self.b_score.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 50pt;font-weight: bold;'
		# 								'border: 0px solid #FFFFFF; background-color:salmon; color:white;}'
		# 								'height: 418px;width: 48px; align:center')
		# 	self.edit = True
