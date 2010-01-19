import globals
from itertools import imap

class Player:
	def __init__(self, color):
		assert color in globals.validColors
		self.color = color
		self.cards = []
		
	def __str__(self):
		return "Player Color: {0}\nPlayer Cards:\n".format(self.color) \
				+ "\n".join(imap(str, self.cards))
		
	def receiveCard(self, card):
		self.cards.append(card)
	
	def dropCards(self, cards):
		assert len(cards) == 3
		for c in cards:
			self.cards.remove(c)
