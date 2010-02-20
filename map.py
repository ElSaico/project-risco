# coding: utf-8
from pygraph.readwrite.markup import read_hypergraph
from random import shuffle
from itertools import cycle
from globals import debug
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
	
	def neighbors(self, t1, t2):
		edge1 = "('{0}', '{1}')".format(t1, t2)
		edge2 = "('{0}', '{1}')".format(t2, t1)
		if edge1 in self.map.edges() \
			or edge2 in self.map.edges():
			return True
		else:
			return False
		
	def reinforce(self, target, army):
		self.territories[target].reinforce(army)
	
	def attack(self, attacker, defender, army):
		assert self.neighbors(attacker, defender)
		self.territories[attacker].attack(self.territories[defender], army)
		
	def relocate(self, source, destination, size):
		assert self.neighbors(source, destination) \
				and (size <= self.territories[source].armySize - self.relocated[source])
		self.territories[source].relocate(self.territories[destination], size)
		# this keeps track of units already relocated in the same turn
		self.relocated[destination] += size
	
	def endTurn(self):
		for c in self.relocated.keys():
			self.relocated[c] = 0
	
	def countries(self):
		return self.map.nodes()	
	def owner(self, t):
		return self.territories[t].owner
	
	def continent(self, c):
		return self.map.edge_links[c]
	
	def continents(self):
		# ordinary edges are represented by ('node1', 'node2')
		return filter(lambda x: x[:2] != "('", self.map.hyperedges())
