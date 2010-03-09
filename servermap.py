from random import shuffle
from itertools import cycle, chain
from json import loads, dumps
from basemap import BaseMap
from territory import Territory

class ServerMap(BaseMap):
	def __init__(self, json, players):
		doc = loads(json)
		BaseMap.__init__(self, doc)
		self._players = players
		self._continents = dict((x["name"], x["countries"]) for x in doc["continents"])
		self._countries = {}
		self._relocated = {}
		countries = list(chain.from_iterable(self._continents.values()))
		for c in countries:
			self._countries[c] = Territory()
			self._relocated[c] = 0
		
		# owners' sorting
		shuffle(countries)
		owners = cycle(players)
		for c in countries:
			self._countries[c].setOwner(owners.next())

	def attack(self, attacker, defender, army):
		assert self.neighbors(attacker, defender)
		return self._countries[attacker].attack(self._countries[defender], army)
		
	def relocate(self, source, destination, size):
		assert self.neighbors(source, destination) \
				and (size <= self._countries[source].armySize - self._relocated[source])
		self._countries[source].relocate(self._countries[destination], size)
		# this keeps track of units already relocated in the same turn
		self._relocated[destination] += size
	
	def endTurn(self):
		for c in self._relocated.keys():
			self._relocated[c] = 0
	
	def exportMap(self):
		struct = {"continents": [], "borders": list(self._borders),
		          "colors": self.colors, "shapes": self.shapes}
		for c in self.continents():
			struct["continents"].append({"name": c,
				                        "bonus": self._bonus[c],
				                    "countries": self._continents[c]})
		return dumps(struct, indent=4)
	
	def toClient(self):
		struct = {"continents": [], "borders": list(self._borders),
		          "colors": self.colors, "shapes": self.shapes}
		for c in self.continents():
			struct["continents"].append({"name": c,
				                        "bonus": self._bonus[c],
				                    "countries": []})
		for ctn in struct["continents"]:
			for cty in self.continent(ctn["name"]):
				ctn["countries"].append({"name": cty,
				                        "owner": self.owner(cty),
				                         "army": self.army(cty)})
		return dumps(struct)
