from json import loads
from basemap import BaseMap
from territory import Territory

class ClientMap(BaseMap):
	def __init__(self, json, players):
		doc = loads(json)
		BaseMap.__init__(self, doc)
		self._players = players
		self._continents = {}
		self._countries = {}
		for ctn in doc["continents"]:
			self._continents[ctn["name"]] = []
			for cty in ctn["countries"]:
				self._continents[ctn["name"]].append(cty["name"])
				self._countries[cty["name"]] = Territory(cty["army"], cty["owner"])
