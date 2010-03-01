from random import randint

class Territory:
	def __init__(self):
		self.armySize = 1
		self.owner = ""
	
	def setOwner(self, owner):
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
				and (self.owner != defender.owner)
		self.armySize -= army
		
		diceAtk = [0, 0, 0]
		diceDef = [0, 0, 0]
		for i in range(army):
			diceAtk[i] = randint(1, 6)
		
		defSize = defender.armySize		
		if defSize > 3:
			defSize = 3
			
		for i in range(defSize):
			diceDef[i] = randint(1, 6)
			
		diceAtk.sort(reverse=True)
		diceDef.sort(reverse=True)
		
		size = min([army, defSize])
		for i in range(size):
			if diceDef[i] >= diceAtk[i]:
				army -= 1
			else:
				defender.armySize -= 1
		
		conquer = None
		if defender.armySize == 0:
			defender.setOwner(self.owner)
			defender.reinforce(army)
			conquer = True
		else:
			self.reinforce(army)
			conquer = False
			
		return (conquer, diceAtk, diceDef)
