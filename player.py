import constants
from itertools import imap

class Player:
	def __init__(self, color):
		assert color in constants.validColors
		self.color = color
		self.cards = []
		
	def __str__(self):
		return "Player Color: %s\nPlayer Cards:\n" % self.color + \
				"\n".join(imap(str, self.cards))
		
	def receiveCard(self, card):
		self.cards.append(card)
