from pygraph.classes.Hypergraph import hypergraph
from random import shuffle
from itertools import cycle
from constants import countries, debug
from territory import Territory

class Map:
	def __init__(self, players):
		self.map = hypergraph()
		self.map.add_hyperedges(countries.keys())
		self.territories = {}
		for continent, lst in countries.items():
			for country in lst:
				self.map.add_node(country)
				self.map.link(country, continent)
				self.territories[country] = Territory()
		# maybe a file with all territory links?
		# or in constants.py...
		
		# owners' sorting
		sort = self.territories.keys()
		shuffle(sort)
		owners = cycle(players)
		for c in sort:
			self.territories[c].setOwner(owners.next())
		if debug:
			for n, t in self.territories.items():
				print n, t.owner
