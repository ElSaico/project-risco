import constants

class Player:
	def __init__(self, color):
		assert color in constants.validColors
		self.color = color
		self.cards = []
		
	def __str__(self):
		str = "Player Color: " + self.color + "\nPlayer Cards: "
		for card in self.cards:
			str += card + " "
		return str
