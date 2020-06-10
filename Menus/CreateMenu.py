from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5.QtMultimedia as M
from MenuButton import MenuButton
# from SeasonButton import SeasonButton
import pandas as pd
import csv
import datetime
import os
import textwrap
# + = []
class CreateMenu(QMainWindow):
	def __init__(self, main):
		super().__init__()
		super().setStyleSheet("QMainWindow {background-image:url(\"assets/jeopBack.png\")}")
		self.main = main
		self.selectedSeason = None
		myCats = ["VIDEO GAME", "ARGENTINA","SOCCER","NBA", "SOUTH AMERICA","BOARD GAME","INTERNET","FICTION"]

		self.searchCats = None
		self.searchQs = None
		# self.real = real
		# if not real:
		# 	self.games = pd.read_excel('Games.xlsx',sheet_name=None)
		# 	self.gameNames = self.games.keys()
		# else:
		# 	self.folderNames = self.loadSeasons()

		self.resize(1500,1200)
		self.refreshMenu()

	def filteredCats(self,filter=None):
		allCats = {filter[i]:set() for i in range(len(filter))}
		searchWithQ = {filter[i]:set() for i in range(len(filter))}
		for s in range(30,36):
			tsv_file = open("Seasons/season"+str(s)+".tsv")
			read_tsv = csv.reader(tsv_file, delimiter="\t")
			for row in read_tsv:
				for cat in filter:
					if cat.lower() in row[3].lower(): allCats[cat].add(row[3].replace("\\",""))
					if cat.lower() in row[5].lower(): searchWithQ[cat].add(row[3].replace("\\",""))

		# print("-----------ALLCATS-----------\n\n")
		# for i in allCats: print(i,allCats[i],"\n\n")
		# print("-----------CATSWITHQ-----------\n\n")
		# for i in searchWithQ: print(i,searchWithQ[i],"\n\n")

		# allCats = list(allCats)
		# for myCat in filter:
		# 	print([allCats[i] for i in range(len(allCats)) if myCat.lower() in allCats[i].lower()])
		return allCats, searchWithQ

	def refreshMenu(self, season=None):
		self.selectedSeason = season
		# self.selectedYear = season.replace()
		goBackBox = QVBoxLayout()
		goBackBox.setAlignment(Qt.AlignLeft)
		backb = QPushButton("Back")
		backb.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 20pt;font-weight: bold;'
									'border: 1px solid #FFFFFF; background-color: transparent; color:white;border-radius: 15px;}'
									'QPushButton:hover { background-color: gray;}'
									'height: 68px;width: 48px; align:center')
		backb.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
		backb.setMaximumSize(100,64)
		backb.setMinimumSize(100,64)

		backb.clicked.connect(lambda: self.main.handle_menustart())
		goBackBox.addWidget(backb)

		title = QVBoxLayout()
		titleLabel = QLabel()
		titleLabel.setStyleSheet("QLabel {background-image:url(\"assets/jeopLogo.png\")}")
		titleLabel.setMinimumSize(863,227)

		title.addWidget(titleLabel)
		title.setAlignment(Qt.AlignCenter)

		searchBox = QHBoxLayout()
		self.search = QLineEdit(self)
		self.search.setMaximumSize(400,60)
		self.search.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
		self.search.setAlignment(QtCore.Qt.AlignCenter)
		self.search.setMinimumSize(400,60)
		self.search.setStyleSheet('QLineEdit {font-family: Arial;font-style: normal;font-size: 50pt;font-weight: bold;'
									'border: 1px solid #FFFFFF; background-color: transparent; color:#b01adb;'
									'border-radius: 10px;}'
									'height: 48px;width: 18px; align:center;')
		f = self.search.font()
		f.setPointSize(35)
		self.search.setFont(f)
		self.search.setPlaceholderText("Search");
		self.search.returnPressed.connect(self.getSearchTerm)


		searchBox.addWidget(self.search)
		scrollArea = QScrollArea()
		scrollArea.setMaximumSize(1200,1000)
		wgtSub = QWidget()
		allSearch = QHBoxLayout(wgtSub)
		allSearch.setSpacing(2)
		count = 5
		searchCol = None
		if self.searchCats:
			for term in list(self.searchCats):
				for cat in self.searchCats[term]:
					if count > 4:
						if searchCol: allSearch.addLayout(searchCol)
						searchCol = QVBoxLayout()
						count = 0
					catButton = MenuButton(self,textwrap.fill(cat,width=15),"search")
					searchCol.addWidget(catButton.button)
					count +=1
			for term in list(self.searchQs):
				for cat in self.searchQs[term]:
					if count > 4:
						if searchCol: allSearch.addLayout(searchCol)
						searchCol = QVBoxLayout()
						count = 0
					catButton = MenuButton(self,textwrap.fill(cat,width=15),"searchQ")
					searchCol.addWidget(catButton.button)
					count +=1
		allSearch.addLayout(searchCol)

		scrollAreaBox = QHBoxLayout()

		scrollArea.setWidget(wgtSub)
		scrollArea.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
		# scrollArea.setFixedSize(800,200)
		scrollArea.setStyleSheet("background-color: transparent;")
		scrollAreaBox.addWidget(scrollArea)

		#
		# 	scrollAreaSeasons.setWidget(wgtSubSeason)
		# 	scrollAreaSeasons.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
		# 	# scrollArea.setFixedSize(800,200)
		# 	scrollAreaSeasons.setStyleSheet("background-color: transparent;")
		# 	scrollAreaSeasonsBox.addWidget(scrollAreaSeasons)
		#
		# scrollArea = None
		# if self.selectedSeason or not self.real:
		# 	if self.real: self.gameNames = self.loadReal(self.selectedSeason)
		# 	scrollArea = QScrollArea()
		# 	scrollArea.setMaximumSize(3000,340)
		# 	wgtSub = QWidget()
		# 	allgamesBox = QVBoxLayout(wgtSub)
		# 	allgamesBox.setSpacing(2)
		# 	count = 1
		# 	gameButtons =  {}
		# 	if self.real:
		# 		button = MenuButton(self,"Season " + self.selectedSeason,"blank")
		# 		allgamesBox.addWidget(button.button)
		# 	else:
		# 		button = MenuButton(self,"Saved Games" ,"blank")
		# 		allgamesBox.addWidget(button.button)
		# 	for game in list(self.gameNames):
		# 		button = MenuButton(self,game,"game")
		# 		allgamesBox.addWidget(button.button)
		# 		count += 1
		# 	scrollAreaBox = QVBoxLayout()
		#
		# 	scrollArea.setWidget(wgtSub)
		# 	scrollArea.setAlignment(Qt.AlignCenter)
		# 	# scrollArea.setFixedSize(800,200)
		# 	scrollArea.setStyleSheet("background-color: transparent;")
		# 	scrollAreaBox.addWidget(scrollArea)
		#
		#
		layout = QVBoxLayout()
		# layout.setSpacing(0)
		layout.addLayout(goBackBox)
		layout.addLayout(searchBox)
		# # layout.addWidget(QLabel(""))
		# # layout.addWidget(QLabel(""))
		# layout.addLayout(title)
		# # layout.addWidget(QLabel(""))
		# # layout.addWidget(QLabel(""))
		# if self.real: layout.addLayout(scrollAreaSeasonsBox)
		if scrollArea: layout.addLayout(scrollAreaBox)
		# if not self.selectedSeason:
		# 	layout.addWidget(QLabel(""))
		# 	layout.addWidget(QLabel(""))
		# 	layout.addWidget(QLabel(""))
		# 	layout.addWidget(QLabel(""))
		# 	layout.addWidget(QLabel(""))
		layout.setAlignment(Qt.AlignCenter )


		self.mainWidget = QWidget()
		self.mainWidget.setLayout(layout)
		self.setCentralWidget(self.mainWidget)

		self.show()

	def getSearchTerm(self):
		self.searchTerm = [self.search.text()]
		self.searchCats, self.searchQs = self.filteredCats(self.searchTerm)
		self.refreshMenu()

	def convDate(self,d):
		return datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%m/%d/%y')

	def loadReal(self, season):
		nameGames = []
		tsv_file = open("Seasons/season"+str(season)+".tsv")
		read_tsv = csv.reader(tsv_file, delimiter="\t")
		for row in read_tsv:
			try:
				if self.convDate(row[7])  not in nameGames: nameGames.append(self.convDate(row[7]))
			except ValueError: pass
		return list(reversed(nameGames))

	def loadSeasons(self):

		return list(reversed([str(i) for i in range(1,36)]))
			# if file.endswith(".txt"):
			#     print(os.path.join("/mydir", file))
