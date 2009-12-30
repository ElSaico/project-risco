from pygraph.classes.hypergraph import hypergraph
from constants import continents, countries, territories
from territory import Territory

class Map:
	def __init__(self):
		self.map = hypergraph()
		self.map.add_nodes(territories)
		self.map.add_hyperedges(continents)
		for continent in continents:
			for country in countries[continent]:
				map.link(country, continent)
		# maybe a file with all territory links?
		# or in constants.py...
		map.add_edge(("Portugal","Spain"))
		# ... and all other edges...
		self.territories = []
		for territory in territories:
			self.territories[territory] = Territory("White")