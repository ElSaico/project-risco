import constants
from random import randint

class Territory:
	def __init__(self, owner):
		# maybe a reference to the map?
		self.setOwner(owner)
		self.armySize = 1
	
	def setOwner(self, owner):
		assert owner in constants.validColors
		self.owner = owner
	
	def reinforce(self, size):
		assert size >= 0
		self.armySize += size
	
	def relocate(self, neighbour, size):
		# verify if the other territory is also yours and a neighbour,
		# if there are enough armies avaliable to relocate, yada, yada,
		# yada. the most boring part by far (btw, the map is the one to
		# keep track of the relocations IMO)
		pass

	def attack(self, defender, army):
		# verify if they're neighbours
		print self.armySize, defender.armySize, army
		assert (1 <= army <= 3) and (army < self.armySize) \
				and (army <= defender.armySize)
		self.armySize -= army
		for i in range(army):
			diceAtk = randint(1, 6)
			diceDef = randint(1, 6)
			if constants.debug:
				print "Dados:", diceAtk, diceDef
			if diceDef >= diceAtk:
				army -= 1
			else:
				defender.armySize -= 1
		if constants.debug:
			print "Ataque:", army, "Defesa:", defender.armySize
		if defender.armySize == 0:
			defender.setOwner(self.owner)
			defender.armySize = army
		else:
			self.reinforce(army)
