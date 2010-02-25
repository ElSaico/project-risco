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
			self.reinforce = self.territoryCount(self.turn) / 2
			for c in self.worldmap.continents():
				if self.ownContinent(self.turn, c):
					self.reinforce += self.map.continentBonus(c)
		elif self.step == "End":
			self.turn = self.players.next().color
			self.step = self.steps.next()
	
	def ownContinent(self, player, continent):
		return all(self.worldmap.owner(x) == player
				for x in self.worldmap.continent(continent))
	
	def territoryCount(self, player):
		return len(filter(lambda x: self.worldmap.owner(x) == self.turn,
									self.worldmap.countries()))
	
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
