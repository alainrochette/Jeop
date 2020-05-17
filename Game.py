import PyQt5
# from Pic import Pic
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from Player import Player
from Question import Question
from ExcelQuestion import ExcelQuestion
import sys
from random import choice, random
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtWidgets import *
import textwrap
import csv
import pandas as pd

SIG=QObject()

_app = QApplication([])
# + = [] {}

class Game(QMainWindow):
	def __init__(self, main, gameName):
		super().__init__()
		super().setStyleSheet("background-color: black")
		self.main = main
		self.gameName = gameName
		self.roundExcelQuestions  = self.loadQuestions()
		# self.ExcelQuestions = ExcelQuestions(gameName)
		self.date = None
		self.all_questions = []
		# self.main.player.stop()
		self.round = 1
		self.questionsGrid = []
		self.player_names = main.player_names


		self.timerTick = 0
		self.startShow  =  [[1,4,0,2,5],
							[3,5,3,1,0],
							[0,2,1,4,3],
							[5,1,4,0,2],
							[2,3,2,5,4],
							[4,0,5,3,1]]
		self.questions = {}

		self.frame = QFrame()
		# self.second_round = []
		self.prize = 0
		self.onQuestion = False
		self.answered = False
		self.currentQ = None
		self.timer = None
		self.categories = ["CATEGORY ONE","CAT2","CAT3","CAT4","CAT5","CAT6"]
		self.answered_questions = []
		self.revealedCats = []
		self.main.players = [Player(self, name) for name in main.player_names]
		self.finalQ =  Question(self,3,100, 100, "Final Category", "FINAL QUESTION", "What is a placeholder.",True)
		# self.resize(1200, 1200)

		self.start_game(load=True)



	def loadQuestions(self):
		excelgame = pd.read_excel('Games.xlsx',sheet_name=self.gameName)
		r = 2
		round = 1

		roundExcelQuestions= {}
		roundExcelQuestions[round]= []
		for index, row in excelgame.iterrows():
			if r == 16 or r == 30:
				round += 1
				roundExcelQuestions[round]= []
			else:
				if r!=1 and r!=2 and r!=15 and r!=16 and r!=29 and r!=30: #SKIP INBETWEEN
					if r % 2 == 0:
						qrow = int(((r -3) % 14)/2)
						# print("ANSROW", qrow)
						colrange = 6 if round < 3 else 1
						for qcol in range(colrange):
							answer = row[qcol] if not pd.isna(row[qcol]) else ""
							# print("QUESTION",roundExcelQuestions[round][qrow][qcol].q_text)
							# print("ANSWER", answer)
							roundExcelQuestions[round][qrow][qcol].a_text = answer
					else:
						isCat = True if (r==3 or r==17 or r==31) else False
						colrange = 6 if round < 3 else 1
						if isCat:
							categories= [row[i] for i in range(colrange)]
							# print("CATEGORIES",categories)


						qrow = int(((r -3) % 14)/2)
						roundQuestionRow = []
						for qcol in range(colrange):
							question = row[qcol]
							# print("ROUND", round, "ROW", qrow, "COL", qcol, "QUEST",question)
							roundQuestionRow.append(ExcelQuestion(self,round,qrow,qcol,categories[qcol],question, "temp"))
						roundExcelQuestions[round].append(roundQuestionRow)
			# print(r, row[0])
			r += 1
		return roundExcelQuestions








	def startFinalJeopardy(self):
		self.round = 3
		self.answered_questions = []
		self.revealedCats = [1,2,3,4,5,6]

		self.start_game()
		self.clickedQ(self.finalQ)

	def startDoubleJeopardy(self):
		self.round = 2
		self.answered_questions = []
		self.revealedCats = []

		self.start_game()
		# super().showNormal()
		# self.showNormal()
		# super().showFullScreen()
		# self.resize(1200, 1200)


	def clickedQ(self, q):
		if len(self.revealedCats)== 6:

			self.prize = q.prize
			self.onQuestion = True
			self.answered = False
			self.answered_questions.append(q.id)
			# q.b.setText = "50000"

			self.layout.deleteLater()
			self.layout.removeItem(self.player_board)

			self.layout = QVBoxLayout()
			self.layout.addLayout(q.qLayout)
			self.layout.addLayout(self.player_board)

			self.mainWidget.deleteLater()
			self.mainWidget = QWidget()
			self.mainWidget.setLayout(self.layout)
			# self.frame.show()
			#
			if q.isDD:
				self.main.ddFX.play()
				q.QGrow()
			else:
				q.QAppear(False)


			self.setCentralWidget(self.mainWidget)

	def revealCat(self, q):
		self.revealedCats.append(q.text)
		self.revealedCats = list(set(self.revealedCats))
		q.b.setText(q.text)
		q.b.clicked.connect(lambda: self.nothing())
		q.b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 24pt;font-weight: bold;'
								'border: 2px solid #FFFFFF; background-color: #000292; color:white;}'
								'height: 418px;width: 48px;')

	def backToBoard(self):
		self.onQuestion = False
		self.player_board.setParent(None)
		self.refreshLayout()


	def fadeAudio(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.setVolume)
		self.timer.start(60)

	def setVolume(self):
		if self.timer:
			self.main.volume -= 5
			if self.main.volume < 0:
				self.timer=None
				self.main.player.stop()
				self.fadeEntrance()
				self.main.volume = 100
			else:
				self.main.player.setVolume(self.main.volume)

	def fadeEntrance(self):
		self.main.entryFX.play()
		self.timerTick = 0
		self.timer = QTimer()
		self.timer.timeout.connect(self.entrance)
		self.timer.start(350)

	def entrance(self):
		if self.timerTick < len(self.startShow):
			r=1
			for c in self.startShow[self.timerTick]:
				self.questionsGrid[r][c].b.setStyleSheet('QPushButton {font-family: Arial Black;font-style: normal;font-size: 50pt;font-weight: bold;'
										'border: 0px solid #FFFFFF; background-color: #000292; color: #eccd4b}'
										'QPushButton:hover { background-color: blue;}'
										'height: 30px;width: 48px;')
				r += 1

		else:
			self.timer = None
		self.timerTick += 1


	def showAnswer(self, q):
		self.answered = True

		q.QAppear(True)
		if q.timer: q.toggleTimer()

	def playerAdd(self, player):
		if player.edit:
			player.addPoints(100)
		else:
			if self.answered and self.onQuestion:
				player.addPoints(self.prize)
				# self.backToBoard()

	def playerRem(self, player):
		if player.edit:
			player.remPoints(100)
		else:
			if self.onQuestion:
				player.remPoints(self.prize)

	def nothing(self):
		pass

	def refreshLayout(self):
		self.board  =QVBoxLayout()

		if not self.gameName:
			# for r in range(6):
			# 	question_row= QHBoxLayout()
			# 	for c in range(6):
			# 		for q in self.all_questions:
			# 			if q.round == self.round and q.r == r and q.c == c:
			# 				question_row.addWidget(q.b)
			# 				break
			#
			# 	self.board.addLayout(question_row)
			pass
		else:
			categories = ["CAT" + str(i) for i in range(6)]
			for eQRow in range(len(self.roundExcelQuestions[self.round])):
				question_row= QHBoxLayout()
				for eQColumn in range(len(self.roundExcelQuestions[self.round][eQRow])):
					eQ = self.roundExcelQuestions[self.round][eQRow][eQColumn]
					q = Question(self, self.round, eQRow, eQColumn, eQ.category, eQ.q_text,eQ.a_text,loading=False)
					question_row.addWidget(q.b)
				self.board.addLayout(question_row)
			#
			# for r in range(6):
			# 	question_row= QHBoxLayout()
			# 	for c in range(6):
			# 		# print(r,c)
			# 		qtxt = "**One might set this linguistic term as a question in lieue of an actual question." if (r == 3 and c == 3 )else "One might set this linguistic term as a question in lieue of an actual question."
			# 		# qtxt = "**One might set this linguistic term as a question in lieue of an actual question."
			# 		q = Question(self, 1, r, c, categories[c],qtxt, "What is a placeholder.",loading=False)
			# 		# q = self.questionsGrid[r][c]
			# 		question_row.addWidget(q.b)
			# 	self.board.addLayout(question_row)

		self.topmenu = self.add_menu()

		self.layout = QVBoxLayout()
		self.layout.addLayout(self.topmenu)
		self.layout.addLayout(self.board)
		self.layout.addLayout(self.player_board)
		self.mainWidget = QWidget()
		self.mainWidget.setLayout(self.layout)
		self.setCentralWidget(self.mainWidget)
		# self.resize(1200, 1200)
		# self.show()

	def loadQ(self):
		pass


	def start_game(self,load=False):
		if not self.gameName:
			# if load: self.loadQ()
			# if self.round != 3: self.board  =QVBoxLayout()
			# self.player_board  =QVBoxLayout()
			# self.topmenu = self.add_menu()
			# for r in range(6):
			# 	question_row= QHBoxLayout()
			# 	for c in range(6):
			# 		for q in self.all_questions:
			# 			if q.round == self.round and q.r == r and q.c == c:
			# 				question_row.addWidget(q.b)
			# 				break
			#
			# 	self.board.addLayout(question_row)
			pass

		else:
			self.questionsGrid = []
			if self.round != 3: self.board  =QVBoxLayout()
			self.player_board  =QVBoxLayout()
			self.topmenu = self.add_menu()
			# categories = ["CAT" + str(i) for i in range(6)]



			# questions = [[str(r) + "-" + str(c) for c in range(6)] for r in range(6)]
			# print(self.roundExcelQuestions)
			for eQRow in range(len(self.roundExcelQuestions[self.round])):
				question_row= QHBoxLayout()
				newquestionrow = []
				for eQColumn in range(len(self.roundExcelQuestions[self.round][eQRow])):
					eQ = self.roundExcelQuestions[self.round][eQRow][eQColumn]
					q = Question(self, self.round, eQRow, eQColumn, eQ.category, eQ.q_text,eQ.a_text,loading=True)
					newquestionrow.append(q)
					question_row.addWidget(q.b)
				self.board.addLayout(question_row)
				self.questionsGrid.append(newquestionrow)
			if self.round!= 3: self.fadeAudio()

			# self.fadeEntrance()
			# if self.round != 3:
			# 	for r in range(6):
			# 		question_row= QHBoxLayout()
			# 		newquestionrow = []
			# 		for c in range(6):
			# 			qtxt = "**One might set this linguistic term as a question in lieue of an actual question." if (r == 3 and c == 3 )else "One might set this linguistic term as a question in lieue of an actual question."
			# 			q = Question(self, r, c, qtxt, "What is a placeholder.",loading=True)
			# 			newquestionrow.append(q)
			# 			question_row.addWidget(q.b)
			# 		self.board.addLayout(question_row)
			# 		self.questionsGrid.append(newquestionrow)


			# list(map(lambda r: list(map(lambda x: question_rows[r].addWidget(self.bQuestion(x)), questions[r])), range(6)))

		players_row = QHBoxLayout()
		players_row.setSpacing(100)

		for player in self.main.players:

			# self.players.append(player)
			player_col = QHBoxLayout()
			player_col.setSpacing(2)


			player_col.addWidget(player.b_rem)
			player_col.addWidget(player.b_name)
			player_col.addWidget(player.b_add)


			players_row.addLayout(player_col)


		player_scores_row= QHBoxLayout()
		player_scores_row.setSpacing(100)
		list(map(lambda p: player_scores_row.addWidget(p.b_score), self.main.players))

		# list(map(lambda x: self.board.addLayout(x), self.question_rows))
		# self.board.addLayout(self.question_rows[1][1])
		self.player_board.addLayout(player_scores_row)
		self.player_board.addLayout(players_row)

		self.layout = QVBoxLayout()
		self.layout.addLayout(self.topmenu)
		if self.round != 3: self.layout.addLayout(self.board)
		self.layout.addLayout(self.player_board)
		self.layout.setSpacing(8)
		# self.layout.addLayout(player_scores_row)
		# self.layout.addLayout(players_row)

		# self.setLayout(self.layout)
		self.mainWidget = QWidget()
		self.mainWidget.setLayout(self.layout)
		self.setCentralWidget(self.mainWidget)
		self.resize(1500,1200)
		self.show()

	def add_menu(self):
		blayout = QHBoxLayout()

		back = QPushButton("Home")
		back.clicked.connect(self.main.handle_menustart)
		back.setStyleSheet('QPushButton {font-family: Arial;font-style: italic;font-size: 5pt;font-weight: thin;'
								'border: 1px solid gray; background-color: black; color:gray;}'
								'QPushButton:hover { background-color: darkblue;}'
								'height: 418px;width: 48px;')
		back.setMaximumHeight(10)


		if self.round == 1:
			dj = QPushButton("Double Jeopardy")
			dj.clicked.connect(self.main.handle_doublejeopardyMenu)
		if self.round == 2:
			dj = QPushButton("Final Jeopardy")
			dj.clicked.connect(self.main.handle_finaljeopardyMenu)
		if self.round == 3:
			dj = QPushButton("End Jeopardy")
			dj.clicked.connect(lambda: self.nothing())
		dj.setStyleSheet('QPushButton {font-family: Arial;font-style: italic;font-size: 5pt;font-weight: thin;'
								'border: 1px solid gray; background-color: black; color:gray;}'
								'QPushButton:hover { background-color: darkblue;}'
								'height: 418px;width: 48px;')
		dj.setMaximumHeight(10)
		blayout.addWidget(back)
		blayout.addWidget(dj)
		blayout.setSpacing(0)
		return blayout
