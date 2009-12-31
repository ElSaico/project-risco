# coding: utf-8
from pygraph.classes.hypergraph import hypergraph
from random import shuffle
from itertools import cycle
from constants import countries, territoryLinks, debug
from territory import Territory

class Map:
	def __init__(self, players):
		self.map = hypergraph()
		self.map.add_hyperedges(countries.keys())
		self.territories = {}
		self.relocated = {}
		for continent, lst in countries.items():
			for country in lst:
				self.map.add_node(country)
				self.map.link(country, continent)
				self.territories[country] = Territory()
				self.relocated[country] = 0
		for link in territoryLinks:
			self.map.add_edge(link)
		
		# owners' sorting
		sort = self.territories.keys()
		shuffle(sort)
		owners = cycle(players)
		for c in sort:
			self.territories[c].setOwner(owners.next())
		if debug:
			for n, t in self.territories.items():
				print n, t.owner
		
		
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