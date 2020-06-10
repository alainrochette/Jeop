
# + = [] {}
import textwrap
class ExcelQuestion:
	def __init__(self, game,round, r,c,category,question_text,answer_text,clue=None):
		self.game = game
		self.round = round
		self.r = r
		self.c = c
		self.category = category
		self.q_text = question_text
		self.a_text = answer_text
		self.clue = None
		if clue == "": clue = None
		if clue:
			self.clue = textwrap.fill(clue,width=27) if clue != "-" else None
