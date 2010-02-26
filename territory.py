import globals
from random import randint

class Territory:
	def __init__(self):
		self.armySize = 1
		self.owner = ""
	
	def setOwner(self, owner):
		assert owner in globals.validColors
		self.owner = owner
	
	def reinforce(self, size):
		assert size >= 0
		self.armySize += size
	
	def relocate(self, neighbour, size):
		assert (0 < size < self.armySize) and (neighbour.owner == self.owner)
		neighbour.reinforce(size)
		self.armySize -= size
		# map checks if the same unit isn't being relocated twice
		# and if they're neighbours

	def attack(self, defender, army):
		# map verifies if they're neighbours
		if globals.debug:
			print self.armySize, defender.armySize, army
		assert (1 <= army <= 3) and (army < self.armySize) \
				and (army <= defender.armySize) and (self.owner != defender.owner)
		self.armySize -= army
		for i in range(army):
			diceAtk = randint(1, 6)
			diceDef = randint(1, 6)
			if globals.debug:
				print "Dados:", diceAtk, diceDef
			if diceDef >= diceAtk:
				army -= 1
			else:
				defender.armySize -= 1
		if defender.armySize == 0:
			defender.setOwner(self.owner)
			defender.reinforce(army)
		else:
			self.reinforce(army)
