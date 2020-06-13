from PyQt5.QtWidgets import *

class MenuButton:
	def __init__(self, menu,name,type, concot=None):
		self.menu = menu
		self.main = menu.main
		self.name = name
		self.concot = concot
		self.button = QPushButton(name)
		self.button.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 30pt;font-weight: bold;'
									'border: 0px solid #FFFFFF; background-color: purple; color:white;border-radius: 15px;}'
									'QPushButton:hover { background-color: #b01adb;}'
									'height: 68px;width: 48px; align:center')
		self.button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)

		if "game" in type:
			self.button.setMinimumSize(300,70)

			if "custom" in type:
				self.button.clicked.connect(lambda: self.button_start_game("custom"))
			else:
				self.button.clicked.connect(lambda: self.button_start_game())
			self.button.setMaximumSize(300,70)
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

			if self.name == "?":
				fsize = "30pt"
				bordercolor = "solid #FFFFFF"
				hovercolor = "#b01adb"
				bgcolor = "purple"
			else:
				self.button.setText(self.name + "  \'" + self.concot.split("||")[2].split("/")[2] )
				fsize = "12pt"
				bordercolor = "solid purple"
				if type == "search":
					hovercolor = "#b01adb"
					bgcolor = "purple"
				if type == "searchQ":
					hovercolor = "pink"
					bgcolor = "transparent"
			style = """QPushButton {font-family: Arial;font-style: normal;font-size: """+fsize+""";font-weight: bold;
										border: 2px """+bordercolor+"""; background-color: """+bgcolor+"""; color:white;border-radius: 15px;}
										QPushButton:hover { background-color: """+hovercolor+""";}
										height: 68px;width: 48px; align:center"""
			self.button.setStyleSheet(style)
			if self.name == "?":
				self.button.clicked.connect(lambda:self.menu.addCustom("?||?||?", random=True))
			else:
				self.button.clicked.connect(lambda:self.menu.addCustom(self.concot, random=False))
			self.button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
			self.button.setMinimumSize(200,88)
			self.button.setMaximumSize(200,88)

		if type == "selectedCat":

			if self.name == "?":
				fsize = "22pt"
			else:
				fsize = "12pt"
				self.button.setText(self.name + "  \'" + self.concot.split("||")[2].split("/")[2])
			style = """QPushButton {font-family: Arial;font-style: normal;font-size: """ + fsize + """;font-weight: bold;
					border: 0px solid #FFFFFF; background-color: #000292; color:white;border-radius: 15px;}
					height: 68px;width: 48px; align:center;"""
			self.button.setStyleSheet(style)
			self.button.clicked.connect(lambda:self.menu.removeCustom(self.concot))
			self.button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
			self.button.setMinimumSize(200,70)
			self.button.setMaximumSize(200,70)
		if type == "separator":
			self.button.setStyleSheet('QPushButton {font-family: Arial;font-style: normal;font-size: 12pt;font-weight: bold;'
												'border: 0px solid #FFFFFF; background-color: salmon; color:white;border-radius: 5px;}'
												# 'QPushButton:hover { background-color: blue;}'
												'height: 68px;width: 48px; align:center')
			self.button.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
			self.button.setMinimumSize(30,70)
			self.button.setMaximumSize(30,70)

		if type == "blank":
			self.button.setMinimumSize(150,50)
			if name == "Seasons:":
				color = "pink"
			else:
				color = "purple"
			style = """QPushButton {font-family: Arial;font-style: normal;font-size: 30pt;font-weight: bold;
						border: 0px solid #FFFFFF; background-color: transparent; color:"""+color+""";border-radius: 15px;}
						height: 68px;width: 48px; align:center"""
			self.button.setStyleSheet(style)

			# self.button.clicked.connect(lambda: self.button_load_season())
	def button_start_game(self, custom=None):
		if custom:
			self.main.handle_gamestart("custom", self.menu.selectedCats)
		else:
			self.main.handle_gamestart(self.button.text(), self.menu.selectedSeason)

	def button_load_season(self):
		self.menu.refreshGames(self.name)
