from random import choice, randint
# from Pic import Pic
import PyQt5
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import *
import textwrap

# + = []

whiteTransition = ["#000292","#000292","#000292","#000292","#0002b3","#0002e0","#1416ff","#5758ff","#7072ff","#bdbeff","white"]
class Question:
	def __init__(self, game,round, r,c,category,question_text,answer_text, loading,):
		self.game = game
		self.round = round
		self.category = category
		self.r = r
		self.c = c
		self.loading = loading


		# self.q_text= question_text

		self.q_text = question_text.replace("**","")
		# if " | " in self.q_text:
			# self.finalCat = self.q_text.split(" | ")[0]
			# self.q_text = self.q_text.split(" | ")[1]
		self.q_text = textwrap.fill(self.q_text,width=40)
		# print(question_text)
		self.isDD = True if  "**" in question_text else False
		self.a_text = str(answer_text)
		self.timer = None
		self.qLayout = QVBoxLayout()
		self.timerCountdown = 6
		# self.q = None
		self.titleLabel = None
		self.qLayout.addLayout(self.menu(self.isDD))
		self.qLayout.addLayout(self.bTimerBox())
		self.qLayout.addLayout(self.bQuestionBox(self.isDD))
		self.qLayout.addLayout(self.bAnswerBox())
		self.qLayout.setSpacing(0)
		self.text = ""
		self.colorindex = 0
		self.transTimer = None
		self.sizeTimer  = None

		self.qsize = 0



		self.id = str(self.game.round)+str(r) + str(c)


		self.revealedCat = False
		self.b = None
		self.b = self.bQuestion()





	def bQuestion(self):
		self.prize = self.game.round * self.r * 200
		self.text = "$" + str(self.prize) if self.r != 0 else textwrap.fill(self.category,width=12)
		if self.id in self.game.answered_questions:
			b = QPushButton("")
			b.clicked.connect(lambda: self.game.nothing())
			b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 40pt;font-weight: bold;'
									'border: 0px solid #FFFFFF; background-color: #000292; color: #eccd4b;}'
									'height: 30px;width: 48px;'
							 )
		elif self.text in self.game.revealedCats:
			b = QPushButton(self.text)
			b.clicked.connect(lambda: self.game.nothing())
			b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 25pt;font-weight: bold;'
									'border: 2px solid #FFFFFF; background-color: #000292; color:white;}'
									'height: 30px;width: 48px;')
			shad = QGraphicsDropShadowEffect();
			shad.setBlurRadius(10);
			shad.setColor(QColor("#000000"));
			shad.setOffset(20,20);
			b.setGraphicsEffect(effect);
		else:
			# self.text = "$" + str(self.prize) if self.r != 0 else textwrap.fill(self.game.categories[self.c],width=5)

			if self.r == 0:
				b = QPushButton("")
				#500066
				b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 30pt;font-weight: bold;'
										'border: 2px solid #FFFFFF; background-color: #000292; color:white;}'
										'QPushButton:hover { background-color: blue;}'
										'height: 30px;width: 48px;')
				b.clicked.connect(lambda: self.game.revealCat(self))
			elif self.loading:
				b = QPushButton(self.text)
				b.setStyleSheet('QPushButton {font-family: Arial Black;font-style: normal;font-size: 50pt;font-weight: bold;'
										'border: 0px solid #FFFFFF; background-color: #000292; color: #000292}'
										# 'QPushButton:hover { background-color: blue;}'
										'height: 30px;width: 48px;')
				b.clicked.connect(lambda: self.game.clickedQ(self))
			else:
				b = QPushButton(self.text)
				b.setStyleSheet('QPushButton {font-family: Arial Black;font-style: normal;font-size: 50pt;font-weight: bold;'
										'border: 0px solid #FFFFFF; background-color: #000292; color:  #eccd4b}'
										'QPushButton:hover { background-color: blue;}'
										'height: 30px;width: 48px;')
				b.clicked.connect(lambda: self.game.clickedQ(self))
		b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		# b.setMaximumSize(200,100)
		return b

	def QAppear(self, ans):
		self.transTimer = QTimer()
		self.transTimer.timeout.connect(lambda:self.changeQColor(ans))
		self.transTimer.start(60)

	def QGrow(self):
		self.sizeTimer = QTimer()
		self.sizeTimer.timeout.connect(lambda:self.changeQSize())
		self.sizeTimer.start(60)

	def changeQSize(self):
		if self.qsize <= 2:
			self.titleLabel.setMaximumSize(900*self.qsize,300)
			self.qsize += 0.1
		else:
			self.sizeTimer  = None


	def changeQColor(self,ans):
		# q.ansb.setText(q.a_text)
		t = whiteTransition

		if self.colorindex < len(t):
			if ans:
				self.ansb.setStyleSheet('QLabel {font-family: Arial;font-style: italic;font-size: 60pt;font-weight: thin;'
									'border: 0px solid #FFFFFF; background-color: #000292; color:'+str(t[self.colorindex])+';}'
									'height: 418px;width: 48px;')
			else:
				self.q.setStyleSheet('QLabel {font-family: Arial;font-style: normal;font-size: 60pt;font-weight: bold;'
										'border: 0px solid #FFFFFF; background-color: #000292; color:'+str(t[self.colorindex])+';}'
										'height: 418px;width: 48px;')
			self.colorindex += 1
		else:
			self.colorindex = 0
			self.transTimer  = None


	def bTimerBox(self):
		blayout = QVBoxLayout()
		self.timerbox = QLabel("")
		self.timerbox.setStyleSheet('QLabel {font-family: Arial;font-style: normal;font-size: 60pt;font-weight: bold;'
								'border: 0px solid #FFFFFF; background-color: #000292; color:#4143c8;}'
								'height: 418px;width: 48px;')
		self.timerbox.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.timerbox.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		self.timerbox.setMaximumHeight(55)
		# self.timerbox.setMinimumHeight(50)
		blayout.addWidget(self.timerbox)
		return blayout

	def bQuestionBox(self, showDDTitle=False):
		blayout = QVBoxLayout()
		if self.isDD and showDDTitle:
			title = QVBoxLayout()

			# titleLabel = QPushButton("DAILY\nDOUBLE")
			self.titleLabel = QLabel()
			self.titleLabel.setStyleSheet("QLabel {background-image:url(\"assets/dailyDoub.png\");"
											"background-color: #000292;}"
											"background-position: top right;"
											"background-repeat: repeat-xy;")
			# titleLabel.setStyleSheet("QPushButton {background-image:url(\"assets/dailyDoub.png\"); background-color: #000292;}'height: 168px")
			# titleLabel.setStyleSheet('QPushButton {font-family: Verdana;font-style: normal;font-size: 140pt;font-weight: bold;'
			# 							'border: 0px solid #FFFFFF; background-color: "#000292"; color:white;}'
			# 							'height: 168px;width: 48px; align:center')
			# titleLabel.setMinimumSize(550,258)
			self.titleLabel.setMaximumSize(0,0)
			self.titleLabel.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
			# titleLabel.clicked.connect(self.showQuestion)

			title.addWidget(self.titleLabel)
			title.setAlignment(Qt.AlignCenter)
			blayout.addLayout(title)
			# blayout.addLayout(playButtonBox)
			blayout.setSpacing(10)

		else:
			if self.round == 3: self.q = QLabel(self.category)
			if self.round != 3: self.q = QLabel(self.q_text)
			self.q.setStyleSheet('QLabel {font-family: Arial;font-style: normal;font-size: 60pt;font-weight: bold;'
									'border: 0px solid #FFFFFF; background-color: #000292; color:#000292;}'
									'height: 418px;width: 48px;')
			self.q.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
			self.q.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
			blayout.addWidget(self.q)
		return blayout

	def bAnswerBox(self, showDDTitle=False):
		blayout = QVBoxLayout()
		if self.isDD and showDDTitle:
			play = QLabel("Wager")
			play.setStyleSheet('QLabel {font-family: Arial;font-style: normal;font-size: 40pt;font-weight: bold;'
										'border: 0px solid #FFFFFF; background-color: #000292; color:white;}'
										'height:418px;width: 48px; align:center')
			play.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
			play.setMinimumSize(300,260)
			# play.clicked.connect(self.showQuestion)
			blayout.addWidget(play)
		else:

			self.ansb = QLabel(self.a_text)
			self.ansb.setStyleSheet('QLabel {font-family: Arial;font-style: italic;font-size: 60pt;font-weight: thin;'
									'border: 0px solid #FFFFFF; background-color: #000292; color:#000292;}'
									'height: 418px;width: 48px;')
			self.ansb.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
			self.ansb.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
			blayout.addWidget(self.ansb)
		return blayout

	def menu(self, showDDTitle=False):
		blayout = QHBoxLayout()

		back = QPushButton("Back")
		if self.r!= 100:
			back = QPushButton("Back")
			back.clicked.connect(lambda: self.game.backToBoard())
		if self.r== 100:
			back = QPushButton("Home")
			back.clicked.connect(lambda: self.game.main.handle_menustart())
		back.setStyleSheet('QPushButton {font-family: Arial;font-style: italic;font-size: 30pt;font-weight: thin;'
								'border: 1px solid gray; background-color: #000292; color:gray;}'
								'QPushButton:hover { background-color: blue;}'
								'height: 418px;width: 48px;')
		back.setMaximumHeight(30)
		blayout.addWidget(back)

		if self.isDD and showDDTitle:
			self.bTimer = QPushButton("Show Question")
			self.bTimer.clicked.connect(lambda: self.showQuestion())
		else:
			self.bTimer = QPushButton("Start Timer")
			if self.r != 100:
				self.bTimer = QPushButton("Start Timer")
				self.bTimer.clicked.connect(lambda: self.toggleTimer())
			if self.r== 100:
				self.bTimer = QPushButton("Show Question")
				self.bTimer.clicked.connect(lambda: self.showFinalQ())
		self.bTimer.setStyleSheet('QPushButton {font-family: Arial;font-style: italic;font-size: 30pt;font-weight: thin;'
								'border: 1px solid gray; background-color: #000292; color:lightgray;}'
								'QPushButton:hover { background-color: blue;}'
								'height: 418px;width: 48px;')

		blayout.addWidget(self.bTimer)


		bShowAns = QPushButton("Show Answer")
		bShowAns.clicked.connect(lambda: self.game.showAnswer(self))
		bShowAns.setStyleSheet('QPushButton {font-family: Arial;font-style: italic;font-size: 30pt;font-weight: thin;'
								'border: 1px solid gray; background-color: #000292; color:gray;}'
								'QPushButton:hover { background-color: blue;}'
								'height: 418px;width: 48px;')
		blayout.addWidget(bShowAns)



		blayout.setSpacing(0)
		bShowAns.setMaximumHeight(30)
		return blayout

	def updateTimer(self):
		if self.timerCountdown <= 0:
			self.timer = None
		else:
			self.timerCountdown -= 1
			try:
				self.timerbox.setText(str(self.timerCountdown))
				if self.timerCountdown==0:
					 self.game.main.tuFX.play()
					 self.toggleTimer()
			except RuntimeError:
				pass


	def toggleTimer(self):
		if self.timer:
			self.bTimer.setText("Start Timer")
			self.timerCountdown = 6
			self.timerbox.setText("")
			self.timer = None
		else:
			self.bTimer.setText("Stop Timer")
			self.timerbox.setText(str(self.timerCountdown))
			self.timer = QTimer()
			self.timer.timeout.connect(self.updateTimer)
			self.timer.start(1000)

	def toggleFinalTimer(self):
		self.game.main.finalTheme.play()


	def showFinalQ(self):
		self.q.setText(self.q_text)
		self.bTimer.setText("Start Timer")
		self.bTimer.clicked.connect(lambda: self.toggleFinalTimer())


	def showQuestion(self):
		self.qLayout = QVBoxLayout()
		self.qLayout.addLayout(self.menu())
		self.qLayout.addLayout(self.bTimerBox())
		self.qLayout.addLayout(self.bQuestionBox())
		self.qLayout.addLayout(self.bAnswerBox())
		self.qLayout.setSpacing(0)
		self.isDD = False
		self.game.clickedQ(self)


	# def show_question(self):
	# 	self.bQuestion
