# coding: utf-8
from random import shuffle
from itertools import cycle, chain
from json import loads, dumps
from territory import Territory

class Map:
	def __init__(self, mapfile, players):
		with open(mapfile) as m:
			self.map = self.load(m.read())
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
		
	def load(self, string):
		doc = loads(string)
		self._borders = set(map(tuple, doc["borders"]))
		self._bonus = dict((x["name"], x["bonus"]) for x in doc["continents"])
		self._continents = dict((x["name"], x["countries"]) for x in doc["continents"])
		self.colors = tuple(doc["colors"])
		self.shapes = tuple(doc["shapes"])

	def __str__(self):
		return "\n".join("{0} - {1.owner}, {1.armySize}".format(n, t)
							for n, t in self._countries.items())
	
	def neighbors(self, t1, t2):
		return (t1, t2) in self._borders or (t2, t1) in self._borders
		
	def reinforce(self, target, army):
		self._countries[target].reinforce(army)
	
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
	
	def country(self, t):
		return self._countries[t]
	
	def countries(self):
		return self._countries.keys()	
	def owner(self, t):
		return self._countries[t].owner
	
	def army(self, t):
		return self._countries[t].armySize
	
	def continent(self, c):
		return self._continents[c]
	
	def continents(self):
		return self._continents.keys()
	
	def continentBonus(self, c):
		return self._bonus[c]
	
	def json(self):
		struct = {"continents": [], "borders": list(self._borders),
		          "colors": self.colors, "shapes": self.shapes}
		for c in self.continents():
			struct["continents"].append({"name": c,
				                        "bonus": self._bonus[c],
				                    "countries": self._continents[c]})
		return dumps(struct, indent=4)	
	def jsonDump(self):
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
