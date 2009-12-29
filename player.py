class Player:
	color = ""
	cards = []
	def __init__(self, _color):
		self.color = _color
		
	def to_s(self):
		return self.color + " player - cards: ..."