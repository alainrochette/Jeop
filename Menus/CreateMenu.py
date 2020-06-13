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
		self.selectedSeason = "Custom"
		self.selectedCats = []
		self.searchCats = []
		self.searchQs = []
		# self.real = real
		# if not real:
		# 	self.games = pd.read_excel('Games.xlsx',sheet_name=None)
		# 	self.gameNames = self.games.keys()
		# else:
		# 	self.folderNames = self.loadSeasons()

		self.resize(1500,1200)
		self.refreshMenu()

	def filteredCats(self,cat=None):
		allCats = {cat:[]}
		searchWithQ = {cat:[]}
		for s in reversed(range(1,36)):
			tsv_file = open("Seasons/season"+str(s)+".csv")
			read_tsv = csv.reader(tsv_file, delimiter=",")
			for row in reversed(list(read_tsv)):
				if (row[0]!='3' and len(self.selectedCats) < 12) or (len(self.selectedCats) == 12 and row[0] == '3'):
					if cat.lower() in row[3].lower().replace("\\",""):
						concot = row[3].replace("\\","").replace("&", "&&") + "||" + str(s) + "||" + datetime.datetime.strptime(row[7], '%Y-%m-%d').strftime('%m/%d/%y')
						if concot not in allCats[cat]: allCats[cat].append(concot)
					if cat.lower() in row[5].lower().replace("\\","") and row[0] != '3':
						concot = row[3].replace("\\","").replace("&", "&&") + "||" + str(s) + "||" + datetime.datetime.strptime(row[7], '%Y-%m-%d').strftime('%m/%d/%y')
						if concot not in searchWithQ[cat]: searchWithQ[cat].append(concot)

		return allCats, searchWithQ

	def refreshMenu(self, clear=True):
		# self.selectedSeason = season
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
									'border: 1px solid #FFFFFF; background-color: transparent; color:white;'
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


		selectedCatsArea = QScrollArea()
		selectedCatsArea.setMaximumSize(1200,100)
		wgtSubCat = QWidget()
		selectedCatsBox = QHBoxLayout(wgtSubCat)
		selectedCatsBox.setSpacing(2)
		# buttonSelected = MenuButton(self,"Selected:","blank")
		# selectedCatsBox.addWidget(buttonSelected.button)
		count = 0
		for concot in list(self.selectedCats):
			if count % 6 == 0:
				round = str((int(count/6))+1)
				sep = MenuButton(self,round,"separator")
				selectedCatsBox.addWidget(sep.button)
			cat = concot.split("||")[0]
			buttonSelected = MenuButton(self,textwrap.fill(cat,width=15),"selectedCat",concot)
			# buttonSeason.button.setMinimumSize(150,50)
			selectedCatsBox.addWidget(buttonSelected.button)
			count += 1

		scrollAreaCatsBox = QHBoxLayout()

		selectedCatsArea.setWidget(wgtSubCat)
		selectedCatsArea.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
		# scrollArea.setFixedSize(800,200)
		selectedCatsArea.setStyleSheet("background-color: transparent;")
		scrollAreaCatsBox.addWidget(selectedCatsArea)




		searchCol = QVBoxLayout()
		if len(self.selectedCats) == 12 and clear:
			self.searchCats, self.searchQs = [],[]
		if len(self.selectedCats) == 13:
			playbutton = MenuButton(self,"Play","customgame")
			searchCol.addWidget(playbutton.button)
		else:
			catButton = MenuButton(self,"?","search")
			searchCol.addWidget(catButton.button)
			count = 1
			for term in list(self.searchCats):
				for concot in self.searchCats[term]:
					cat = concot.split("||")[0]
					s = concot.split("||")[1]
					d = concot.split("||")[2]
					if count > 4:
						if searchCol: allSearch.addLayout(searchCol)
						searchCol = QVBoxLayout()
						count = 0
					catButton = MenuButton(self,textwrap.fill(cat,width=15),"search", cat + "||" + s + "||" + d)

					searchCol.addWidget(catButton.button)
					count +=1
			for term in list(self.searchQs):
				for concot in self.searchQs[term]:
					cat = concot.split("||")[0]
					s = concot.split("||")[1]
					d = concot.split("||")[2]
					if count > 4:
						if searchCol: allSearch.addLayout(searchCol)
						searchCol = QVBoxLayout()
						count = 0
					catButton = MenuButton(self,textwrap.fill(cat,width=15),"searchQ", cat + "||" + s + "||" + d)
					searchCol.addWidget(catButton.button)
					count +=1
		allSearch.addLayout(searchCol)

		scrollAreaBox = QHBoxLayout()

		scrollArea.setWidget(wgtSub)
		scrollArea.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
		# scrollArea.setFixedSize(800,200)
		scrollArea.setStyleSheet("background-color: transparent;")
		scrollAreaBox.addWidget(scrollArea)
		layout = QVBoxLayout()
		# layout.setSpacing(0)

		layout.addLayout(goBackBox)

		layout.addLayout(searchBox)
		layout.addLayout(scrollAreaCatsBox)
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
		if len(self.search.text()) > 2:
			self.searchCats, self.searchQs = self.filteredCats(self.search.text())
			self.refreshMenu(False)

	def convDate(self,d):
		return datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%m/%d/%y')

	def loadReal(self, season):
		nameGames = []
		tsv_file = open("Seasons/season"+str(season)+".csv")
		read_tsv = csv.reader(tsv_file, delimiter=",")
		for row in read_tsv:
			try:
				if self.convDate(row[7])  not in nameGames: nameGames.append(self.convDate(row[7]))
			except ValueError: pass
		return list(reversed(nameGames))

	def loadSeasons(self):
		return list(reversed([str(i) for i in range(1,36)]))

	def addCustom(self,concot, random):
		if len(self.selectedCats) < 13 and (concot not in self.selectedCats or "?" in concot):
			self.selectedCats.append(concot)
			self.refreshMenu()

	def removeCustom(self, concot):
		self.selectedCats.remove(concot)
		self.refreshMenu()
			# if file.endswith(".txt"):
			#     print(os.path.join("/mydir", file))
