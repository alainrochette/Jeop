import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Game import Game
from Player import Player
from Menus.Menu import Menu
from Menus.LoadMenu import LoadMenu
from Menus.CreateMenu import CreateMenu
from Menus.DoubMenu import DoubMenu
from Menus.FinalMenu import FinalMenu
import PyQt5.QtMultimedia as M

import csv
import os
import sys


_app = QApplication([])


class Communicate(QObject):
	gamestart = pyqtSignal()
	menustart = pyqtSignal()

COM = Communicate()

# + = [] {}
class MainWindow(QWidget):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.game = None
		self.soundsList = ["jeopTheme", "dailyDouble", "timesUp", "jeopFinal","jeopEntry"]
		self.soundVolumes = {"jeopTheme":10, "dailyDouble":40, "timesUp":60, "jeopFinal":100,"jeopEntry":100}
		self.menu = Menu(self)
		self.loadmenu= None
		self.doubMenu=None
		self.finalMenu=None
		self.players  = []
		self.player_names = []
		self.me = None
		self.comp = None
		self.prob_verdad = 1
		self.difficulty = 1.5
		self.history = []
		self.lying_rate = 0
		self.buffer = 1
		self.setFixedSize(1200,1200);
		self.in_game = False

		# self.maxvolume = 100
		self.volume = 10
		self.sounds = {}


		COM.menustart.connect(self.handle_menustart)
		COM.menustart.emit()




	def handle_menustart(self):
		if "jeopTheme" in self.sounds:
			self.sounds["jeopTheme"].setVolume(self.soundVolumes["jeopTheme"])
			self.sounds["jeopTheme"].play()
		if self.game: self.game.hide()
		if self.loadmenu: self.loadmenu.hide()
		if "jeopFinal" in self.sounds: self.sounds["jeopFinal"].stop()
		self.menu.show()
		self.hide()
		self.on_menu = True

	def handle_loadmenustart(self, type=None):
		if self.menu: self.menu.hide()
		if self.game: self.game.hide()
		if "jeopFinal" in self.sounds: self.sounds["jeopFinal"].stop()
		if type == "Create":
			self.loadmenu = CreateMenu(self)
		else:
			real = True if type == "Real" else False
			self.loadmenu = LoadMenu(self, real)
		self.hide()

	def handle_gamestart(self,gameName,season=None):
		if self.menu: self.menu.hide()
		if self.loadmenu: self.loadmenu.hide()
		if self.game: self.game.deleteLater()
		self.game = Game(self,gameName,season)

	def handle_doublejeopardy(self):
		# if self.menu: self.menu.hide()
		if self.DoubMenu: self.DoubMenu.hide()
		# if self.game: self.game.hide()
		self.game.startDoubleJeopardy()

	def handle_doublejeopardyMenu(self):
		if self.menu: self.menu.hide()
		if self.game: self.game.hide()
		self.DoubMenu = DoubMenu(self)

	def handle_finaljeopardy(self):
		if self.menu: self.menu.hide()
		if self.finalMenu: self.finalMenu.hide()

		self.game.startFinalJeopardy()

	def handle_finaljeopardyMenu(self):
		if self.menu: self.menu.hide()
		if self.game: self.game.hide()
		self.finalMenu = FinalMenu(self)


if __name__ == '__main__':
	if "--install" in sys.argv:
		os.system("clear")
		print("---- Installing pip ----\n")
		os.system("curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py")
		os.system("python3 get-pip.py")
		print("---- Installing Interface ----\n")
		os.system("python3 -m pip install PyQt5")
		print("---- Installing Pandas ----\n")
		os.system("pip install pandas")
		# if sys.platform == "darwin":
		#     print("\n---- Installing XCode Command Line Tools ----\n")
		#     os.system("xcode-select --install")


	_main_window = MainWindow()


	for s in _main_window.soundsList:
		filename= 'assets/' + s + '.mp3'
		fullpath = QDir.current().absoluteFilePath(filename)
		media = QUrl.fromLocalFile(fullpath)
		content = M.QMediaContent(media)
		_main_window.sounds[s] = M.QMediaPlayer()
		_main_window.sounds[s].setMedia(content)
		_main_window.sounds[s].setVolume(_main_window.soundVolumes[s])
		if s == "jeopTheme":_main_window.sounds[s].play()

	sys.exit(_app.exec_())
