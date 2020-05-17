import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Game import Game
from Player import Player
from Menus.Menu import Menu
from Menus.LoadMenu import LoadMenu
from Menus.DoubMenu import DoubMenu
from Menus.FinalMenu import FinalMenu
# from Menu import Menu
# from LoadMenu import LoadMenu
# from DoubMenu import DoubMenu
# from FinalMenu import FinalMenu
# from own_dice import OwnDice
import PyQt5.QtMultimedia as M

import csv

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
		# self.own_dice = False

		# self.resize(800, 600)
		# self.resize(1200,1200)
		self.setFixedSize(1200,1200);
		self.in_game = False
		self.player = None
		self.finalTheme = None
		self.volume = 100


		COM.menustart.connect(self.handle_menustart)

		# COM.gamestart.connect(lambda: self.handle_gamestart())
		COM.menustart.emit()




	def handle_menustart(self):
		if self.player:
			self.volume = 100
			self.player.setVolume(100)
			self.player.play()
		if self.game: self.game.hide()
		if self.loadmenu: self.loadmenu.hide()
		if self.finalTheme: self.finalTheme.stop()
		self.menu.show()
		self.hide()
		self.on_menu = True

	def handle_loadmenustart(self):
		if self.menu: self.menu.hide()
		if self.game: self.game.hide()
		if self.finalTheme: self.finalTheme.stop()
		self.loadmenu = LoadMenu(self)
		self.hide()

	def handle_gamestart(self,game):
		if self.menu: self.menu.hide()
		if self.loadmenu: self.loadmenu.hide()
		if self.game: self.game.deleteLater()

		self.game = Game(self,game)

	def handle_doublejeopardy(self):
		if self.menu: self.menu.hide()
		if self.DoubMenu: self.DoubMenu.hide()
		# if self.game: self.game.deleteLater()

		self.game.startDoubleJeopardy()

	def handle_doublejeopardyMenu(self):
		if self.menu: self.menu.hide()
		if self.game: self.game.hide()
		self.DoubMenu = DoubMenu(self)

	def handle_finaljeopardy(self):
		if self.menu: self.menu.hide()
		if self.finalMenu: self.finalMenu.hide()
		# if self.game: self.game.deleteLater()

		self.game.startFinalJeopardy()

	def handle_finaljeopardyMenu(self):
		if self.menu: self.menu.hide()
		if self.game: self.game.hide()
		self.finalMenu = FinalMenu(self)


		# self.game = Window(self)





if __name__ == '__main__':

	_main_window = MainWindow()
	filenameTheme= 'assets/jeopTheme.mp3'
	fullpathTheme = QDir.current().absoluteFilePath(filenameTheme)
	mediaTheme = QUrl.fromLocalFile(fullpathTheme)
	contentTheme = M.QMediaContent(mediaTheme)

	filenameDD= 'assets/dailyDouble.mp3'
	fullpathDD = QDir.current().absoluteFilePath(filenameDD)
	mediaDD = QUrl.fromLocalFile(fullpathDD)
	contentDD = M.QMediaContent(mediaDD)

	filenameTU= 'assets/timesUp.mp3'
	fullpathTU = QDir.current().absoluteFilePath(filenameTU)
	mediaTU = QUrl.fromLocalFile(fullpathTU)
	contentTU = M.QMediaContent(mediaTU)

	filenameFinal= 'assets/jeopFinal.mp3'
	fullpathFinal = QDir.current().absoluteFilePath(filenameFinal)
	mediaFinal = QUrl.fromLocalFile(fullpathFinal)
	contentFinal = M.QMediaContent(mediaFinal)

	filenameEntry= 'assets/jeopEntry.mp3'
	fullpathEntry = QDir.current().absoluteFilePath(filenameEntry)
	mediaEntry = QUrl.fromLocalFile(fullpathEntry)
	contentEntry = M.QMediaContent(mediaEntry)



	_main_window.ddFX = M.QMediaPlayer()
	_main_window.ddFX.setMedia(contentDD)

	_main_window.tuFX = M.QMediaPlayer()
	_main_window.tuFX.setMedia(contentTU)

	_main_window.entryFX = M.QMediaPlayer()
	_main_window.entryFX.setMedia(contentEntry)

	_main_window.finalTheme = M.QMediaPlayer()
	_main_window.finalTheme.setMedia(contentFinal)

	_main_window.player = M.QMediaPlayer()
	_main_window.player.setMedia(contentTheme)
	_main_window.player.play()



	sys.exit(_app.exec_())
