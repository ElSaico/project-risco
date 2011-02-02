# coding: utf-8

class BaseMap:
	def __init__(self, doc):
		self._borders = set(map(tuple, doc["borders"]))
		self._bonus = dict((x["name"], x["bonus"]) for x in doc["continents"])
		self.colors = tuple(doc["colors"])
		self.shapes = tuple(doc["shapes"])
		
	def __str__(self):
		return "\n".join("{0} - {1.owner}, {1.armySize}".format(n, t)
							for n, t in self._countries.items())
	
	def neighbors(self, t1, t2):
		return (t1, t2) in self._borders or (t2, t1) in self._borders
		
	def reinforce(self, target, army):
		self._countries[target].reinforce(army)
		
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
		
