from PyQt5.QtWidgets import *

class MenuButton:
	def __init__(self, menu,name,type):
		self.menu = menu
		self.main = menu.main
		self.name = name
		self.button = QPushButton(name)
		self.button.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 30pt;font-weight: bold;'
									'border: 0px solid #FFFFFF; background-color: purple; color:white;border-radius: 15px;}'
									'QPushButton:hover { background-color: #b01adb;}'
									'height: 68px;width: 48px; align:center')
		self.button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

		if type == "game":
			self.button.setMinimumSize(300,70)
			self.button.clicked.connect(lambda: self.button_start_game())
		if type == "season":
			self.button.setText(str(int(self.name) + 1983))
			self.button.setMinimumSize(200,50)
			self.button.clicked.connect(lambda: self.button_load_season())
		if type == "normal":
			self.button.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 40pt;font-weight: bold;'
										'border: 0px solid #FFFFFF; background-color: purple; color:white;border-radius: 15px;}'
										'QPushButton:hover { background-color: #b01adb;}'
										'height: 68px;width: 48px; align:center')
			self.button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
			self.button.setMinimumSize(300,88)
		if "search" in type:
			if type == "search": self.button.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;'
										'border: 0px solid #FFFFFF; background-color: purple; color:white;border-radius: 15px;}'
										'QPushButton:hover { background-color: #b01adb;}'
										'height: 68px;width: 48px; align:center')
			if type == "searchQ": self.button.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;'
										'border: 2px solid purple; background-color: transparent; color:white;border-radius: 15px;}'
										'QPushButton:hover { background-color: pink;}'
										'height: 68px;width: 48px; align:center')
			self.button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
			self.button.setMinimumSize(200,88)
			self.button.setMaximumSize(200,88)
		if type == "blank":
			self.button.setMinimumSize(150,50)
			if name == "Seasons:":
				self.button.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 30pt;font-weight: bold;'
											'border: 0px solid #FFFFFF; background-color: transparent; color:pink;border-radius: 15px;}'
											# 'QPushButton:hover { background-color: #b01adb;}'
											'height: 68px;width: 48px; align:center')
			else:
				self.button.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 30pt;font-weight: bold;'
											'border: 0px solid #FFFFFF; background-color: transparent; color:purple;border-radius: 15px;}'
											# 'QPushButton:hover { background-color: #b01adb;}'
											'height: 68px;width: 48px; align:center')
			# self.button.clicked.connect(lambda: self.button_load_season())

	def button_start_game(self):
		self.main.handle_gamestart(self.button.text(), self.menu.selectedSeason)

	def button_load_season(self):
		self.menu.refreshGames(self.name)
