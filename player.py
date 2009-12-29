class Player:
	cards = []
	def __init__(self, color):
		self.color = color
		
	def __str__(self):
		return self.color + " player - cards: ..."
