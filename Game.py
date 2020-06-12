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
import datetime
import random

SIG=QObject()

_app = QApplication([])
# + = [] {}

class Game(QMainWindow):
	def __init__(self, main, gameName, season=None):
		super().__init__()
		super().setStyleSheet("background-color: black")
		self.main = main
		self.gameName = gameName
		self.season = season
		self.selectedCats = None
		if gameName == "custom":
			self.selectedCats = season
			self.roundExcelQuestions = self.loadCustom()

		elif gameName.count("/") == 2:
			self.roundExcelQuestions  = self.loadRealQuestions()
		else:
			self.roundExcelQuestions  = self.loadQuestions()
		self.date = None
		self.all_questions = []
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
		self.prize = 0
		self.onQuestion = False
		self.answered = False
		self.currentQ = None
		self.timer = None
		self.categories = ["CATEGORY ONE","CAT2","CAT3","CAT4","CAT5","CAT6"]
		self.answered_questions = []
		self.revealedCats = []
		self.main.players = [Player(self, name) for name in main.player_names]
		# self.cleanSeasons()
		self.start_game(load=True)

	def loadCustom(self):
		roundExcelQuestions= {}
		round = 1
		ncats = 0
		for concot in self.selectedCats:
			nqs = 0
			cat = concot.split("||")[0]
			s = concot.split("||")[1]
			d = concot.split("||")[2]
			if concot == "?||?||?": s = str(random.randint(1,35))

			if ncats == 6:
				ncats = 0
				round += 1
			if ncats == 0:
				if round < 3: roundExcelQuestions[round]=  [["X" for i in range(6)] for i in range(6)]
				if round == 3: roundExcelQuestions[round]=  [["X"]]
			# print("BEFORE", round,ncats, nqs)
			tsv_file = open("Seasons/season"+str(s)+".csv")
			read_tsv = csv.reader(tsv_file, delimiter=",")
			roundQuestionRow = []
			if cat == "?":
				row_count = sum([1 for row in read_tsv])
				tsv_file.close()
				tsv_file = open("Seasons/season"+str(s)+".csv")
				read_tsv = csv.reader(tsv_file, delimiter=",")
				start_row = random.randint(1,row_count - 9)
				rcount = 0
				prev = ""
				starting = False
				for row in read_tsv:
					# print(rcount,start_row)
					if rcount >= start_row and (round == 3 or round != 3 and row[0]!='3'):
						if nqs == 5:
							break
						fcat = row[3].replace("\\", "")
						if prev == "": prev = fcat
						if prev != fcat or starting:
							starting = True
							if nqs == 0:
								roundExcelQuestions[round][nqs][ncats] = ExcelQuestion(self,round,0,ncats,fcat,fcat, "cat",row[4]+ "  \'" + str(datetime.datetime.strptime(row[7], '%Y-%m-%d').strftime('%m/%d/%y').split("/")[2]))
							if round != 3: nqs += 1
							q = row[5].replace("\\", "")
							if row[2] == 'yes': q = "**" + q
							a = row[6].replace("\\", "")
							roundExcelQuestions[round][nqs][ncats] = ExcelQuestion(self,round,nqs,ncats,fcat, q,a,row[4]+ "  \'" + str(datetime.datetime.strptime(row[7], '%Y-%m-%d').strftime('%m/%d/%y').split("/")[2]))
					rcount +=1
				if nqs == 5:
					nqs = 0
					ncats += 1
			else:
				for row in read_tsv:
					if nqs == 5:
						break
					fcat = row[3].replace("\\", "")
					fd = self.convDate(row[7])
					if cat == fcat and d == fd:

						if nqs == 0:
							roundExcelQuestions[round][nqs][ncats] = ExcelQuestion(self,round,0,ncats,cat ,cat, "cat",row[4]+ "  \'" + str(datetime.datetime.strptime(row[7], '%Y-%m-%d').strftime('%m/%d/%y').split("/")[2]))
						if round != 3: nqs += 1
						q = row[5].replace("\\", "")
						if row[2] == 'yes': q = "**" + q
						a = row[6].replace("\\", "")
						roundExcelQuestions[round][nqs][ncats] = ExcelQuestion(self,round,nqs,ncats,cat, q,a,row[4]+ "  \'" + str(datetime.datetime.strptime(row[7], '%Y-%m-%d').strftime('%m/%d/%y').split("/")[2]))
				if nqs == 5:
					nqs = 0
					ncats += 1

		for round in range(1,3):
			totalDJ = 0
			for r in range(5):
				for c in range(6):
					if "**" in  roundExcelQuestions[round][r][c].q_text:
						if totalDJ == round:
							roundExcelQuestions[round][r][c].q_text = roundExcelQuestions[round][r][c].q_text.replace("**","")
						else:
							totalDJ +=1
			while totalDJ != round:
				randr = random.randint(1,5)
				randc = random.randint(1,5)
				if "**" not in roundExcelQuestions[round][randr][randc].q_text:
					roundExcelQuestions[round][randr][randc].q_text = "**" + roundExcelQuestions[round][randr][randc].q_text
					totalDJ += 1
		return roundExcelQuestions

	def loadQuestions(self):
		excelgame = pd.read_excel('Games.xlsx',sheet_name=self.gameName)
		r = 2
		round = 1

		roundExcelQuestions= {}
		roundExcelQuestions[round]= []
		for index, row in excelgame.iterrows():
			if r > 34: break
			if r == 16 or r == 30:
				round += 1
				roundExcelQuestions[round]= []
			else:
				if r!=1 and r!=2 and r!=15 and r!=16 and r!=29 and r!=30: #SKIP INBETWEEN
					if r % 2 == 0:
						qrow = int(((r -3) % 14)/2)
						colrange = 6 if round < 3 else 1
						for qcol in range(colrange):
							answer = row[qcol] if not pd.isna(row[qcol]) else ""
							roundExcelQuestions[round][qrow][qcol].a_text = answer
							if isCat: roundExcelQuestions[round][qrow][qcol].clue = textwrap.fill(answer,width=27)
					else:
						isCat = True if (r==3 or r==17 or r==31) else False
						colrange = 6 if round < 3 else 1
						if isCat: categories= [row[i] for i in range(colrange)]

						qrow = int(((r -3) % 14)/2)
						roundQuestionRow = []
						for qcol in range(colrange):
							question = row[qcol]
							roundQuestionRow.append(ExcelQuestion(self,round,qrow,qcol,categories[qcol],question, "cat",))
						roundExcelQuestions[round].append(roundQuestionRow)

			r += 1
		return roundExcelQuestions

	def getRow(self, round, prize):
		return int((prize / round) / 200)


	# def cleanSeasons(self):
	# 	catCount = {}
	# 	for s in range(1,36):
	# 		tsv_file = open("Clean Seasons/season"+str(s)+".tsv")
	# 		read_tsv = csv.reader(tsv_file, delimiter="\t")
	#
	#
	# 		for row in read_tsv:
	# 			dt = self.convDate(row[7])
	# 			cat = row[3].replace("\\", "")
	# 			concot = dt + cat
	# 			if concot not in catCount:
	# 				catCount[concot] = 0
	# 			catCount[concot] += 1
	# 		tsv_file.close()
	# 	for s in range(1,36):
	# 		tsv_file = open("Clean Seasons/season"+str(s)+".tsv")
	# 		output = open("Clean Seasons/clean_season" + str(s)+ ".csv", 'a', newline='')
	# 		read_tsv = csv.reader(tsv_file, delimiter="\t")
	# 		write_tsv = csv.writer(output, dialect='excel')
	# 		checkedConcots = []
	# 		for row in read_tsv:
	# 			dt = self.convDate(row[7])
	# 			cat = row[3].replace("\\", "")
	# 			concot = dt + cat
	# 			if catCount[concot] == 5 or row[0] == '3':
	# 				# print(row)
	# 				write_tsv.writerow(row)


		# return roundExcelQuestions

	def loadRealQuestions(self):
		tsv_file = open("Seasons/season"+str(self.season)+".csv")
		# tsv_file = open("Seasons/season"+str(self.season)+".tsv")
		read_tsv = csv.reader(tsv_file, delimiter=",")


		roundExcelQuestions= {}
		roundExcelQuestions[1] = [["X" for i in range(6)] for i in range(6)]
		roundExcelQuestions[2] = [["X" for i in range(6)] for i in range(6)]
		roundExcelQuestions[3] = [["X"]]

		dateRounds = {}
		for row in read_tsv:
			# print(row[0])
			dt = self.convDate(row[7])
			if dt == "XXX": continue
			round = int(row[0])
			cat = row[3].replace("\\", "")
			if dt not in dateRounds:
				dateRounds[dt] = {}
			if round not in dateRounds[dt]:
				dateRounds[dt][round] = {}
			if cat not in dateRounds[dt][round]:
				dateRounds[dt][round][cat] = []
				dateRounds[dt][round][cat].append(ExcelQuestion(self,round,0, 100,cat, cat,"cat", row[4]))
			q = row[5].replace("\\", "")
			a = row[6].replace("\\", "")
			if row[2] == 'yes':
				r = (r + 1) % 6
				q = "**" + q
			else:
				if datetime.datetime.strptime(row[7], '%Y-%m-%d') <= datetime.datetime.strptime("2001-11-23", '%Y-%m-%d'):
					r = int((int(row[1]) / int(row[0])) / 100)
				else:
					r = int((int(row[1]) / int(row[0])) / 200)
			dateRounds[dt][round][cat].append(ExcelQuestion(self,round,r, 100,cat, q,a, row[4]))
		alldates = list(dateRounds.keys())
		totalcats = {}
		totalcats[1] = 0
		totalcats[2] = 0
		totalcats[3] = 0
		for r in dateRounds[self.gameName]:
			for cat in dateRounds[self.gameName][r]:
				if len(dateRounds[self.gameName][r][cat]) == 6 or r == 3:
					for q in dateRounds[self.gameName][r][cat]:
						roundExcelQuestions[r][q.r][totalcats[r]] = q
					totalcats[r] += 1

		nextD = self.gameName
		for r in roundExcelQuestions:
			if r < 3:
				for cat in roundExcelQuestions[r]:
					while totalcats[r] < 6:
						nextD = alldates[(alldates.index(nextD) + 1) % (len(alldates))]
						for round in dateRounds[nextD]:
							if r == round:
								for cat in dateRounds[nextD][r]:
									if len(dateRounds[nextD][r][cat]) == 6 or r == 3:
										for q in dateRounds[nextD][r][cat]:
											roundExcelQuestions[r][q.r][totalcats[r]] = q
										totalcats[r] += 1
										if totalcats[r] >= 6: break
					# 		if totalcats[r] >= 6: break
					# 	if totalcats[r] >= 6: break
					# if totalcats[r] >= 6: break

		return roundExcelQuestions


	def convDate(self,d):
		try:
			return datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%m/%d/%y')
		except ValueError:
			return "XXX"

	def startFinalJeopardy(self):
		super().__init__()
		super().setStyleSheet("background-color: black")
		self.round = 3
		self.answered_questions = []
		self.revealedCats = [1,2,3,4,5,6]

		self.start_game()
		try:
			eQ = self.roundExcelQuestions[self.round][1][0]
		except IndexError:
			eQ = self.roundExcelQuestions[self.round][0][0]
		q = Question(self, self.round, eQ.r, eQ.c, eQ.category, eQ.q_text,eQ.a_text,loading=False)
		self.clickedQ(q)

	def startDoubleJeopardy(self):
		super().__init__()
		super().setStyleSheet("background-color: black")
		self.round = 2
		self.answered_questions = []
		self.revealedCats = []
		self.main.resize(1500,1200)
		# self.show()
		self.start_game()

	def clickedQ(self, q):
		# print(self.revealedCats)
		if len(self.revealedCats)>= 6:

			self.prize = q.prize
			self.onQuestion = True
			self.answered = False
			self.answered_questions.append(q.id)

			self.layout.deleteLater()
			self.layout.removeItem(self.player_board)

			self.layout = QVBoxLayout()
			self.layout.addLayout(q.qLayout)
			self.layout.addLayout(self.player_board)

			self.mainWidget.deleteLater()
			self.mainWidget = QWidget()
			self.mainWidget.setLayout(self.layout)

			if q.isDD:
				self.main.sounds["dailyDouble"].play()
				# self.main.ddFX.play()
				q.QGrow()
			else:
				q.QAppear(False)


			self.setCentralWidget(self.mainWidget)

	def revealCat(self, q):
		self.revealedCats.append(q.text)
		self.revealedCats = list(set(self.revealedCats))
		q.b.setText(q.text)
		if len(q.clue) > 5:
			q.b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;'
									'border: 2px solid yellow; background-color: #000292; color:white;}'
									'QPushButton:hover { background-color: blue;}'
									'height: 418px;width: 48px;')
			q.b.clicked.connect(lambda: q.toggleClue())
		else:
			# q.b.clicked.connect(lambda: self.nothing())
			q.b.clicked.connect(lambda: q.toggleClue())
			if len(q.clue) > 0:
				q.b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;'
										'border: 2px solid #FFFFFF; background-color: #000292; color:white;}'
										'QPushButton:hover { background-color: blue;}'
										'height: 418px;width: 48px;')
			else:
				q.b.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;'
										'border: 2px solid #FFFFFF; background-color: #000292; color:white;}'
										'height: 418px;width: 48px;')

	def backToBoard(self):
		self.onQuestion = False
		self.player_board.setParent(None)
		self.refreshLayout()


	def fadeAudio(self):
		self.timer = QTimer()
		self.main.volume = self.main.soundVolumes["jeopTheme"]
		self.timer.timeout.connect(self.setVolume)
		self.timer.start(60)

	def setVolume(self):
		if self.timer:
			self.main.volume -= 1
			if self.main.volume < 0:
				self.timer=None
				self.main.sounds["jeopTheme"].stop()
				self.fadeEntrance()
				self.main.volume = 100
			else:
				self.main.sounds["jeopTheme"].setVolume(self.main.volume)

	def fadeEntrance(self):
		self.main.sounds["jeopEntry"].setVolume(self.main.soundVolumes["jeopEntry"]/2)
		self.main.sounds["jeopEntry"].play()
		self.timerTick = 0
		self.timer = QTimer()
		self.timer.timeout.connect(self.entrance)
		self.timer.start(350)

	def entrance(self):
		if self.round == 3:
			self.timer = None
		else:
			if self.timerTick < len(self.startShow):
				r=1
				self.main.sounds["jeopEntry"].setVolume(min((self.main.soundVolumes["jeopEntry"]/2)*(1 + (1/2)*self.timerTick),100))
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
		if (self.round ==3 and q.showedFinal) or self.round != 3:
			self.answered = True
			q.QAppear(True)
			if q.timer: q.toggleTimer()
			if self.round == 3:
				q.bShowAns.setText("Finish")
				q.bShowAns.clicked.connect(self.main.handle_endjeopardyMenu)

	def playerAdd(self, player):
		if player.edit:
			player.addPoints(100)
		else:
			if self.answered and self.onQuestion:
				player.addPoints(self.prize)

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

		for eQRow in range(len(self.roundExcelQuestions[self.round])):
			question_row= QHBoxLayout()
			for eQColumn in range(len(self.roundExcelQuestions[self.round][eQRow])):
				eQ = self.roundExcelQuestions[self.round][eQRow][eQColumn]
				q = Question(self, self.round, eQRow, eQColumn, eQ.category, eQ.q_text,eQ.a_text,False,eQ.clue)
				question_row.addWidget(q.b)
			self.board.addLayout(question_row)

		self.topmenu = self.add_menu()

		self.layout = QVBoxLayout()
		self.layout.addLayout(self.topmenu)
		self.layout.addLayout(self.board)
		self.layout.addLayout(self.player_board)
		self.mainWidget = QWidget()
		self.mainWidget.setLayout(self.layout)
		self.setCentralWidget(self.mainWidget)

	def loadQ(self):
		pass


	def start_game(self,load=False):
		self.questionsGrid = []
		if self.round != 3: self.board  =QVBoxLayout()
		self.player_board  =QVBoxLayout()
		self.topmenu = self.add_menu()

		# print(self.roundExcelQuestions)

		for eQRow in range(len(self.roundExcelQuestions[self.round])):
			question_row= QHBoxLayout()
			newquestionrow = []
			for eQColumn in range(len(self.roundExcelQuestions[self.round][eQRow])):
				eQ = self.roundExcelQuestions[self.round][eQRow][eQColumn]
				q = Question(self, self.round, eQRow, eQColumn, eQ.category, eQ.q_text,eQ.a_text,True,eQ.clue)
				newquestionrow.append(q)
				question_row.addWidget(q.b)
			self.board.addLayout(question_row)
			self.questionsGrid.append(newquestionrow)
		if self.round!= 3: self.fadeAudio()

		player_scores_row= QHBoxLayout()
		player_scores_row.setSpacing(32)
		list(map(lambda p: player_scores_row.addWidget(p.b_score), self.main.players))

		players_row = QHBoxLayout()
		players_row.setSpacing(30)

		for player in self.main.players:
			player_col = QHBoxLayout()
			player_col.setSpacing(2)

			player_col.addWidget(player.b_rem)
			player_col.addWidget(player.b_name)
			player_col.addWidget(player.b_add)

			players_row.addLayout(player_col)



		self.player_board.addLayout(player_scores_row)
		self.player_board.addLayout(players_row)

		self.layout = QVBoxLayout()
		self.layout.addLayout(self.topmenu)
		if self.round != 3: self.layout.addLayout(self.board)
		self.layout.addLayout(self.player_board)
		self.layout.setSpacing(8)

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
		# back.setMaximumWidth(300)


		if self.round == 1:
			dj = QPushButton("Double Jeopardy")
			dj.clicked.connect(self.main.handle_doublejeopardyMenu)
		if self.round == 2:
			dj = QPushButton("Final Jeopardy")
			dj.clicked.connect(self.main.handle_finaljeopardyMenu)
		if self.round == 3:
			dj = QPushButton("End Jeopardy")
			dj.clicked.connect(self.main.handle_endjeopardyMenu)
		dj.setStyleSheet('QPushButton {font-family: Arial;font-style: italic;font-size: 5pt;font-weight: thin;'
								'border: 1px solid gray; background-color: black; color:gray;}'
								'QPushButton:hover { background-color: darkblue;}'
								'height: 418px;width: 48px;')
		dj.setMaximumHeight(10)
		# dj.setMaximumWidth(300)
		blayout.addWidget(back)
		blayout.addWidget(dj)
		blayout.setSpacing(0)
		return blayout
