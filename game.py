from random import shuffle
from itertools import cycle
from map import Map

class Game:
	def __init__(self):
		self.players = []
		self.worldmap = None
		self.turn = None
		
	def addPlayer(self, player):
		if not player in self.players:
			self.players.append(player)
	
	def setup(self):
		colors = [x.color for x in self.players]
		self.worldmap = Map(colors)
		shuffle(self.players)
		self.players = cycle(self.players)
		self.turn = self.players.next().color
		
	def start(self):
		# game action here
		print self.turn + "'s turn."
