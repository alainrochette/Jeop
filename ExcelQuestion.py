
# + = [] {}

class ExcelQuestion:
	def __init__(self, game,round, r,c,category,question_text,answer_text,):
		self.game = game
		self.round = round
		self.r = r
		self.c = c
		self.category = category
		self.q_text = question_text
		self.a_text = answer_text

		# print(excelgame.loc[[0]])
