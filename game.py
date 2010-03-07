from random import shuffle
from itertools import cycle
from map import Map

class Game:
	players = []
	turnCount = 1
	steps = cycle(("Trade", "Reinforce", "Attack", "Relocate", "End"))
	
	def __init__(self, mapfile, globalTrade):
		self.globalTrade = globalTrade
		self.reinforcements = 0
		self._mapfile = mapfile
	
	def addPlayer(self, player):
		if not player in self.players:
			self.players.append(player)
	
	def start(self):
		colors = (x.color for x in self.players)
		self.worldmap = Map(self._mapfile, colors)
		shuffle(self.players)
		self.players = cycle(self.players)
		self.turn = self.players.next().color
		self.nextStep()
	
	def nextStep(self):
		self.step = self.steps.next()
		print self.step
		if self.step == "Trade":
			self.reinforcements = self.territoryCount(self.turn) / 2
			if self.reinforcements < 3:
				self.reinforcements = 3
			# TODO: make it continent-only
			#for c in self.worldmap.continents():
			#	if self.ownContinent(self.turn, c):
			#		self.reinforce += self.map.continentBonus(c)
		elif self.step == "End":
			self.turn = self.players.next().color
			self.reinforcements = 0
			self.nextStep()
	
	def ownCountry(self, player, country):
		return self.worldmap.owner(country) == player
	
	def ownContinent(self, player, continent):
		return all(self.ownCountry(player, x)
				for x in self.worldmap.continent(continent))
	
	def territoryCount(self, player):
		return len(filter(lambda x: self.ownCountry(player, x),
									self.worldmap.countries()))
									
	def trade(self, cards): # not tested yet
		assert len(cards) == 3
		if Card.match(cards):		
			for c in cards:
				if not c.wild and self.worldmap.ownCountry(self.turn, c.name):
					self.worldmap.reinforce(c.name, 2)
			# more reinforcements here
	
	def reinforce(self, target, army):
		assert self.worldmap.owner(target) == self.turn and army <= self.reinforcements
		self.worldmap.reinforce(target, army)
		self.reinforcements -= army
	
	def attack(self, attacker, defender, army):
		assert self.worldmap.owner(attacker) == self.turn \
		   and self.worldmap.owner(defender) != self.turn \
		   and self.step == "Attack"
		return self.worldmap.attack(attacker, defender, army)
	
	def relocate(self, source, destination, army):
		assert self.worldmap.owner(source) == self.turn \
		   and self.worldmap.owner(destination) == self.turn \
		   and self.step == "Relocate"
		self.worldmap.relocate(source, destination, army)
	
	def mapDump(self):
		return self.worldmap.jsonDump()
