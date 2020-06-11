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
# + = []
class LoadMenu(QMainWindow):
	def __init__(self, main, real):
		super().__init__()
		super().setStyleSheet("QMainWindow {background-image:url(\"assets/jeopBack.png\")}")
		self.main = main
		self.selectedSeason = None
		self.real = real
		if not real:
			self.games = pd.read_excel('Games.xlsx',sheet_name=None)
			self.gameNames = self.games.keys()
		else:
			self.folderNames = self.loadSeasons()

		self.resize(1500,1200)
		self.refreshGames()


	def refreshGames(self, season=None):
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

		if self.real:
			scrollAreaSeasons = QScrollArea()
			scrollAreaSeasons.setMaximumSize(1200,100)
			wgtSubSeason = QWidget()
			allSeasonsBox = QHBoxLayout(wgtSubSeason)
			allSeasonsBox.setSpacing(2)
			folderButtons =  {}
			buttonSeason = MenuButton(self,"Seasons:","blank")
			allSeasonsBox.addWidget(buttonSeason.button)
			for folder in list(self.folderNames):
				buttonSeason = MenuButton(self,folder,"season")
				# buttonSeason.button.setMinimumSize(150,50)
				allSeasonsBox.addWidget(buttonSeason.button)
			scrollAreaSeasonsBox = QHBoxLayout()

			scrollAreaSeasons.setWidget(wgtSubSeason)
			scrollAreaSeasons.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
			# scrollArea.setFixedSize(800,200)
			scrollAreaSeasons.setStyleSheet("background-color: transparent;")
			scrollAreaSeasonsBox.addWidget(scrollAreaSeasons)

		scrollArea = None
		if self.selectedSeason or not self.real:
			if self.real: self.gameNames = self.loadReal(self.selectedSeason)
			scrollArea = QScrollArea()
			scrollArea.setMaximumSize(3000,340)
			wgtSub = QWidget()
			allgamesBox = QVBoxLayout(wgtSub)
			allgamesBox.setSpacing(2)
			count = 1
			gameButtons =  {}
			if self.real:
				button = MenuButton(self,"Season " + self.selectedSeason,"blank")
				allgamesBox.addWidget(button.button)
			else:
				button = MenuButton(self,"Saved Games" ,"blank")
				allgamesBox.addWidget(button.button)
			for game in list(self.gameNames):
				button = MenuButton(self,game,"game")
				allgamesBox.addWidget(button.button)
				count += 1
			scrollAreaBox = QVBoxLayout()

			scrollArea.setWidget(wgtSub)
			scrollArea.setAlignment(Qt.AlignCenter)
			# scrollArea.setFixedSize(800,200)
			scrollArea.setStyleSheet("background-color: transparent;")
			scrollAreaBox.addWidget(scrollArea)


		layout = QVBoxLayout()
		layout.setSpacing(0)
		layout.addLayout(goBackBox)
		# layout.addWidget(QLabel(""))
		# layout.addWidget(QLabel(""))
		layout.addLayout(title)
		# layout.addWidget(QLabel(""))
		# layout.addWidget(QLabel(""))
		if self.real: layout.addLayout(scrollAreaSeasonsBox)
		if scrollArea: layout.addLayout(scrollAreaBox)
		if not self.selectedSeason:
			layout.addWidget(QLabel(""))
			layout.addWidget(QLabel(""))
			layout.addWidget(QLabel(""))
			layout.addWidget(QLabel(""))
			layout.addWidget(QLabel(""))
		layout.setAlignment(Qt.AlignCenter )


		self.mainWidget = QWidget()
		self.mainWidget.setLayout(layout)
		self.setCentralWidget(self.mainWidget)

		self.show()
	def convDate(self,d):
		return datetime.datetime.strptime(d, '%Y-%m-%d').strftime('%m/%d/%y')

	def loadReal(self, season):
		nameGames = []
		tsv_file = open("Clean Seasons/clean_season"+str(season)+".csv")
		read_tsv = csv.reader(tsv_file, delimiter=",")
		for row in read_tsv:
			try:
				if self.convDate(row[7])  not in nameGames: nameGames.append(self.convDate(row[7]))
			except ValueError: pass
		return list(reversed(nameGames))

	def loadSeasons(self):

		return list(reversed([str(i) for i in range(1,36)]))
			# if file.endswith(".txt"):
			#     print(os.path.join("/mydir", file))
