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
			self.step = self.steps.next()
			self.reinforcements = 0
	
	def ownCountry(self, player, country):
		return self.worldmap.owner(country) == player
	
	def ownContinent(self, player, continent):
		return all(self.ownCountry(player, x)
				for x in self.worldmap.continent(continent))
	
	def territoryCount(self, player):
		return len(filter(lambda x: self.ownCountry(player, x),
									self.worldmap.countries()))
									
	def trade(self, cards):
		cardsCount = {"Circle": 0, "Square": 0, "Triangle": 0, "All": 0}
		for c in cards:
			cardsCount[c.shape] += 1
		
		# maybe trying to find a more elegant way to check this...
		assert cardsCount["Circle"] == 3 or cardsCount["Square"] == 3 or cardsCount["Triangle"] == 3 \
				or cardsCount["Circle"] + cardsCount["All"] == 3 \
				or cardsCount["Square"] + cardsCount["All"] == 3 \
				or cardsCount["Triangle"] + cardsCount["All"] == 3 \
				or (cardsCount["Circle"] == 1 and cardsCount["Square"] == 1 and cardsCount["Triangle"] == 1) \
				or (cardsCount["Circle"] == 1 and cardsCount["Square"] == 1 and cardsCount["All"] == 1) \
				or (cardsCount["Circle"] == 1 and cardsCount["All"] == 1 and cardsCount["Triangle"] == 1) \
				or (cardsCount["All"] == 1 and cardsCount["Square"] == 1 and cardsCount["Triangle"] == 1)
		
		for c in cards:
			if c.name in filter(lambda x: self.worldmap.owner(x) == self.turn, self.worldmap.countries()):
				self.worldmap.territories[c.name].reinforce(2)
	
	def reinforce(self, target, army):
		assert self.worldmap.owner(target) == self.turn and army <= self.reinforcements
		self.worldmap.reinforce(target, army)
		self.reinforcements -= army
	
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
