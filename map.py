# coding: utf-8
from pygraph.readwrite.markup import read_hypergraph
from random import shuffle
from itertools import cycle
from constants import debug
from territory import Territory

class Map:
	def __init__(self, players):
		with open("map.xml") as m:
			self.map = read_hypergraph(m.read())
		self.territories = {}
		self.relocated = {}
		for c in self.map.nodes():
			self.territories[c] = Territory()
			self.relocated[c] = 0
		
		# owners' sorting
		sort = self.map.nodes()
		shuffle(sort)
		owners = cycle(players)
		for c in sort:
			self.territories[c].setOwner(owners.next())
		if debug:
			print self
		
	def __str__(self):
		return "\n".join("{0} - {1.owner}, {1.armySize}".format(n, t)
							for n, t in self.territories.items())
		
	def attack(self, attacker, defender, army):
		assert attacker in self.map.neighbors(defender)
		self.territories[attacker].attack(self.territories[defender], army)
		
	def relocate(self, source, destination, size):
		assert (source in self.map.neighbors(destination)) \
				and (size <= self.territories[source].armySize - self.relocated[source])
		self.territories[source].relocate(self.territories[destination], size)
		# this keeps track of units already relocated in the same turn
		self.relocated[destination] += size
	
	def endTurn(self):
		for c in self.relocated.keys():
			self.relocated[c] = 0
	
	def countries(self):
		return self.map.nodes()
