from pygraph.classes.hypergraph import hypergraph
from constants import continents, countries, territories
from territory import Territory

class Map:
	def __init__(self):
		self.map = hypergraph()
		self.map.add_hyperedges(continents)
		self.territories = {}
		for continent, lst in continents.items():
			for country in lst:
				self.map.add_node(country)
				self.map.link(country, continent)
				self.territories[country] = Territory("White")
		# maybe a file with all territory links?
		# or in constants.py...
		map.add_edge(("Portugal","Inglaterra"))
		# ... and all other edges...
		
