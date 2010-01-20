from random import shuffle
from itertools import cycle
from map import Map

class Game:
	players = []
	turnCount = 1
	steps = cycle(("Trade", "Reinforce", "Attack", "Relocate", "End"))
	
	def __init__(self, globalTrade):
		self.globalTrade = globalTrade
	
	def addPlayer(self, player):
		if not player in self.players:
			self.players.append(player)
	
	def start(self):
		colors = (x.color for x in self.players)
		self.worldmap = Map(colors)
		shuffle(self.players)
		self.players = cycle(self.players)
		self.turn = self.players.next().color
		self.nextStep()
	
	def nextStep(self):
		self.step = self.steps.next()
		if self.step == "Trade":
			self.reinforce = len(filter(
									lambda x: self.worldmap.owner(x) == self.turn,
									self.worldmap.countries())) / 2
			for c in self.worldmap.continents():
				if all(self.worldmap.owner(x) == self.turn
						for x in self.worldmap.continent(c)):
					# continental bonus: where to store it is still undefined
					# hypergraphs don't export edge attributes :(
					pass
		elif self.step == "End":
			self.turn = self.players.next().color
			self.step = self.steps.next()
	
	def reinforce(self, target, army):
		assert self.worldmap.owner(target) == self.turn and army <= self.reinforce
		self.worldmap.reinforce(target, army)
		self.reinforce -= army
	
	def attack(self, attacker, defender, army):
		assert self.worldmap.owner(attacker) == self.turn \
		   and self.worldmap.owner(defender) != self.turn \
		   and self.step == "Attack"
		self.worldmap.attack(attacker, defender, army)
	
	def relocate(self, source, destination, army):
		assert self.worldmap.owner(source) == self.turn \
		   and self.worldmap.owner(destination) == self.turn \
		   and self.step == "Relocate"
		self.worldmap.relocate(source, destination, army)
