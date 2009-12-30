import constants

class Player:
	cards = []
	def __init__(self, color):
		#same code used in territory.py's setOwner, maybe it'd be good to create a function to check this
		if color in constants.validColors:
			self.color = color
		else:
			raise Exception("Invalid color.")
		
	def __str__(self):
		str = "Player Color: " + self.color + "\nPlayer Cards: "
		for card in self.cards:
			str += card + " "
		return str
