from random import choice, randint
# from Pic import Pic
import PyQt5
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtGui import QColor as qc
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import *
import textwrap
import PyQt5.QtMultimedia as M

# + = []

whiteTransition = ["#000292","#000292","#000292","#000292","#0002b3","#0002e0","#1416ff","#5758ff","#7072ff","#bdbeff","white"]
class Question:
	def __init__(self, game,round, r,c,category,question_text,answer_text, loading,clue=None):
		self.game = game
		self.round = round
		self.category = category
		self.r = r
		self.c = c
		self.q = None
		self.showedFinal = False
		self.loading = loading
		# self.clue = clue
		if clue: self.clue = clue.replace("- ","")
		if not clue: self.clue = ""
		self.song = None
		self.songQ = None
		self.songA = None
		question_text = str(question_text)
		answer_text = str(answer_text)
		self.a_text = answer_text
		if ".mp3" in answer_text:
			self.a_text = answer_text.split("Sounds/")[0]
			filename= "Sounds/" +answer_text.split("Sounds/")[1]
			# filename='assets/dailyDouble.mp3'
			fullpath = QDir.current().absoluteFilePath(filename)
			media = QUrl.fromLocalFile(fullpath)
			content = M.QMediaContent(media)

			self.songA= M.QMediaPlayer()
			self.songA.setMedia(content)
		if ".mp3" in question_text:
			self.q_text = question_text.split("Sounds/")[0]
			filename= "Sounds/" +question_text.split("Sounds/")[1]
			# filename='assets/dailyDouble.mp3'
			fullpath = QDir.current().absoluteFilePath(filename)
			media = QUrl.fromLocalFile(fullpath)
			content = M.QMediaContent(media)

			self.songQ= M.QMediaPlayer()
			self.songQ.setMedia(content)
		else:
			self.q_text = question_text.replace("**","")

		self.q_text = textwrap.fill(self.q_text,width=40) if "Pictures/" not in self.q_text else self.q_text
		self.a_text =textwrap.fill(self.a_text,width=40) if "Pictures/" not in self.a_text else self.a_text
		self.song = self.songQ

		# print(question_text)
		self.isDD = True if  "**" in question_text else False


		self.timer = None
		self.qLayout = QVBoxLayout()
		self.timerCountdown = 6

		self.titleLabel = None
		self.bShowAns = None
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


		self.id = str(self.round)+str(r) + str(c)

		self.revealedCat = False
		self.b = None
		self.b = self.bQuestion()





	def bQuestion(self):
		self.prize = self.round * self.r * 200
		if self.r == 0:
			wrapwidth = 12 if len(self.q_text) <= 35 else 20
		self.text = "$" + str(self.prize) if self.r != 0 else textwrap.fill(self.category,width=wrapwidth)
		# print(self.text)
		if self.id in self.game.answered_questions:
			b = QPushButton(self.text)
			b.clicked.connect(lambda: self.game.clickedQ(self))
			b.setStyleSheet('QPushButton {font-family: Arial Black;font-style: normal;font-size: 50pt;font-weight: bold;'
									'border: 0px solid #FFFFFF; background-color: #000292; color: #000292}'
									# 'QPushButton:hover { background-color: blue;}'
									'height: 30px;width: 48px;')
		elif self.text in self.game.revealedCats:
			b = QPushButton(self.text)
			fsize = "15pt" if len(self.q_text) > 35 else "20pt"
			if len(self.clue) > 5:
				bordercolor = "solid yellow"
				hovercolor = "blue"
			else:
				bordercolor = "solid #FFFFFF"
				hovercolor = "#000292"
				if len(self.clue) > 0:
					hovercolor = "blue"

			style = """QPushButton {font-family: Arial ;font-style: normal;font-size: """+fsize+""";font-weight: bold;
						border: 2px """+bordercolor+"""; background-color: #000292; color:white;}
						QPushButton:hover { background-color: """+hovercolor+""";}
						height: 30px;width: 48px;"""
			b.setStyleSheet(style)
			b.clicked.connect(lambda: self.toggleClue())


		else:
			if self.r == 0:
				b = QPushButton("")
				font = "Arial"
				fsize = "24pt"
				bordersize = "2px"
				fcolor = "white"
				hovercolor = "blue"
				b.clicked.connect(lambda: self.game.revealCat(self))
			else:
				b = QPushButton(self.text)
				font = "Arial Black"
				fsize = "50pt"
				bordersize = "0px"
				fcolor = "#eccd4b"
				hovercolor = "blue"
				if self.loading:
					fcolor = "#000292"
					hovercolor = "#000292"
				b.clicked.connect(lambda: self.game.clickedQ(self))

			style = """QPushButton {font-family: """+font+""" ;font-style: normal;font-size: """+fsize+""";font-weight: bold;
						border: """+bordersize+""" solid #FFFFFF; background-color: #000292; color:"""+fcolor+"""}
						QPushButton:hover { background-color: """+hovercolor+""";}
						height: 30px;width: 48px;"""
			b.setStyleSheet(style)
		b.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        # b.setMaximumSize(100,50)
		return b

	def QAppear(self, ans, FinalQ=False):
		self.transTimer = QTimer()
		self.qsize = 0
		if self.song and not ans:
			self.toggleTimer()
		if self.songA and ans: self.changeQVolume(True, self.songA)
		if (FinalQ and "Pictures/" in self.q_text) or (self.round<3 and ("Pictures/" in self.q_text and not ans)) or (self.round < 3 and "Pictures/" in self.a_text and ans):
			self.transTimer.timeout.connect(lambda:self.changeQSize(ans))
			if  "Pictures/" in self.a_text and ans: self.qsize = 1
		else:
			if self.song and ans: self.song.stop()
			self.transTimer.timeout.connect(lambda:self.changeQColor(ans))
		self.transTimer.start(60)


	def changeQVolume(self, up, songA=None):
		song = self.song if not songA else songA
		if up:
			self.game.main.volume = 0
			song.setVolume(0)
			song.play()
		self.transTimer = QTimer()
		self.transTimer.timeout.connect(lambda:self.fadeV(up,song))
		self.transTimer.start(60)

	def fadeV(self, up,song):
		inc = 3 if up else -5
		self.game.main.volume += inc
		if (up and self.game.main.volume > 100) or ((not up) and self.game.main.volume < 0):
			self.transTimer=None
			self.game.main.volume = 100
			if not up: song.stop()
		else:
			song.setVolume(self.game.main.volume)




	def QGrow(self):
		self.sizeTimer = QTimer()
		self.sizeTimer.timeout.connect(lambda:self.changeQSize())
		self.sizeTimer.start(60)

	def changeQSize(self,ans=False):
		q_or_a = self.a_text if ans else self.q_text
		if self.qsize <= 1:
			if "Pictures/" in q_or_a:
				img = QImage(q_or_a).scaledToHeight(400*self.qsize)
				self.q.setPixmap(QPixmap.fromImage(img))
				self.q.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
			else:
				img = QImage("assets/dailyDoub.png").scaledToHeight(250*self.qsize)
				self.titleLabel.setPixmap(QPixmap.fromImage(img))
				# self.titleLabel.setMaximumSize(1255,300)
				self.titleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
			self.qsize += 0.1
		else:
			self.sizeTimer  = None


	def changeQColor(self,ans):
		t = whiteTransition

		if self.colorindex < len(t):
			if ans:
				self.ansb.setStyleSheet('QLabel {font-family: Arial;font-style: italic;font-size: 60pt;font-weight: thin;'
									'border: 0px solid #FFFFFF; background-color: #000292; color:'+str(t[self.colorindex])+';}'
									'height: 418px;width: 48px;')
			elif ("Pictures/" not in self.q_text) or (self.round == 3):
				self.q.setStyleSheet('QLabel {font-family: Times;font-style: normal;font-size: 60pt;font-weight: bold;'
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
		blayout.addWidget(self.timerbox)
		return blayout

	def bQuestionBox(self, showDDTitle=False):
		blayout = QVBoxLayout()
		if self.isDD and showDDTitle:
			title = QVBoxLayout()

			self.titleLabel = QLabel()
			self.titleLabel.setStyleSheet("background-color: #000292;")
			img = QImage("assets/dailyDoub.png").scaledToHeight(0)
			self.titleLabel.setPixmap(QPixmap.fromImage(img))


			# self.titleLabel.setMaximumSize(0,300)
			self.titleLabel.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

			# title.addWidget(self.titleLabel)
			self.titleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
			blayout.addWidget(self.titleLabel)
			blayout.setSpacing(10)

		else:
			if self.round == 3:
				if self.q:
					self.q = QLabel()
					self.q.setStyleSheet("background-color: #000292;")
					img = QImage(self.q_text).scaledToHeight(0)
					self.q.setPixmap(QPixmap.fromImage(img))
					self.q.setAlignment(Qt.AlignCenter)
				else:
					self.q = QLabel(self.category)
					self.q.setStyleSheet('QLabel {font-family: Times;font-style: normal;font-size: 60pt;font-weight: bold;'
											'border: 0px solid #FFFFFF; background-color: #000292; color:#000292;}'
											'height: 418px;width: 48px;')
			else:
				if "Pictures/" in self.q_text:
					self.q = QLabel()
					self.q.setStyleSheet("background-color: #000292;")
					img = QImage(self.q_text).scaledToHeight(0)
					self.q.setPixmap(QPixmap.fromImage(img))
					self.q.setAlignment(Qt.AlignCenter)
				else:
					self.q = QLabel(self.q_text)
					self.q.setStyleSheet('QLabel {font-family: Times;font-style: normal;font-size: 60pt;font-weight: bold;'
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

	def backToBoard(self):
		if self.songA: self.changeQVolume(False, self.songA)
		if self.songQ: self.changeQVolume(False, self.songQ)
		self.game.backToBoard()

	def menu(self, showDDTitle=False):
		blayout = QHBoxLayout()

		# back = QPushButton("Back")
		if self.round != 3:
			back = QPushButton("Back")
			back.clicked.connect(lambda: self.backToBoard())
		if self.round == 3:
			back = QPushButton("Back")
			# back.clicked.connect(lambda: self.game.main.handle_menustart())
			back.clicked.connect(lambda: self.game.nothing())
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
			# self.bTimer = QPushButton("Start Timer")
			if self.round != 3:
				self.bTimer = QPushButton("Start Timer")
				self.bTimer.clicked.connect(lambda: self.toggleTimer())
			if self.round == 3:
				self.bTimer = QPushButton("Show Question")
				self.bTimer.clicked.connect(lambda: self.showFinalQ())
		self.bTimer.setStyleSheet('QPushButton {font-family: Arial;font-style: italic;font-size: 30pt;font-weight: thin;'
								'border: 1px solid gray; background-color: #000292; color:lightgray;}'
								'QPushButton:hover { background-color: blue;}'
								'height: 418px;width: 48px;')

		blayout.addWidget(self.bTimer)


		self.bShowAns = QPushButton("Show Answer")
		self.bShowAns.clicked.connect(lambda: self.showAnswer())
		self.bShowAns.setStyleSheet('QPushButton {font-family: Arial;font-style: italic;font-size: 30pt;font-weight: thin;'
								'border: 1px solid gray; background-color: #000292; color:gray;}'
								'QPushButton:hover { background-color: blue;}'
								'height: 418px;width: 48px;')
		blayout.addWidget(self.bShowAns)



		blayout.setSpacing(0)
		self.bShowAns.setMaximumHeight(30)
		return blayout

	def showAnswer(self):
		if (self.round ==3 and self.showedFinal) or self.round != 3:
			self.game.answered = True
			self.QAppear(True)
			if self.timer: self.toggleTimer()
			if self.round == 3:
				self.bShowAns.setText("Finish")
				self.bShowAns.clicked.connect(self.game.main.handle_endjeopardyMenu)

	def updateTimer(self):
		if self.timerCountdown <= 0:
			self.timer = None
		else:
			self.timerCountdown -= 1
			try:
				self.timerbox.setText(str(self.timerCountdown))
				if self.timerCountdown==0:
					self.game.main.sounds["timesUp"].play()
					self.toggleTimer()
			except RuntimeError:
				pass


	def toggleTimer(self):
		if self.timer:
			self.bTimer.setText("Start Timer")
			self.timerCountdown = 6
			self.timerbox.setText("")
			if self.song: self.changeQVolume(False)
			self.timer = None
		else:
			self.bTimer.setText("Stop Timer")
			self.timerbox.setText(str(self.timerCountdown))
			self.timer = QTimer()
			if self.song: self.changeQVolume(True)
			self.timer.timeout.connect(self.updateTimer)
			self.timer.start(1000)

	def toggleFinalTimer(self):
		self.game.main.sounds["jeopFinal"].play()


	def showFinalQ(self):
		if not self.showedFinal:
			self.showedFinal = True
			if "Pictures/" not in self.q_text:
				self.q.setText(self.q_text)
			self.q.setStyleSheet('QLabel {font-family: Times;font-style: normal;font-size: 60pt;font-weight: bold;'
									'border: 0px solid #FFFFFF; background-color: #000292; color:#000292;}'
									'height: 418px;width: 48px;')
			self.QAppear(False,True)


		self.bTimer.setText("Start Timer")
		self.bTimer.clicked.connect(lambda: self.toggleFinalTimer())


	def toggleClue(self):
		if len(self.clue) > 5:
			if self.b.text() == self.clue:
				self.b.setText(self.text)
				self.b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;'
										'border: 2px solid yellow; background-color: #000292; color:white;}'
										'QPushButton:hover { background-color: blue;}'
										'height: 418px;width: 48px;')
			else:
				self.b.setText(self.clue)
				self.b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;'
										'border: 2px solid yellow; background-color: #000292; color:yellow;}'
										'QPushButton:hover { background-color: blue;}'
										'height: 418px;width: 48px;')
		elif len(self.clue) > 0:
			if self.b.text() == self.clue:
				self.b.setText(self.text)
				self.b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;'
										'border: 2px solid #FFFFFF; background-color: #000292; color:white;}'
										'QPushButton:hover { background-color: blue;}'
										'height: 418px;width: 48px;')
			else:
				self.b.setText(self.clue)
				self.b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 25pt;font-weight: bold;'
										'border: 2px solid #FFFFFF; background-color: #000292; color:yellow;}'
										'QPushButton:hover { background-color: blue;}'
										'height: 418px;width: 48px;')


	def showQuestion(self):
		self.qLayout = QVBoxLayout()
		self.qLayout.addLayout(self.menu())
		self.qLayout.addLayout(self.bTimerBox())
		self.qLayout.addLayout(self.bQuestionBox())
		self.qLayout.addLayout(self.bAnswerBox())
		self.qLayout.setSpacing(0)
		self.isDD = False
		self.game.clickedQ(self)
