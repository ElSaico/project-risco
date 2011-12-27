from random import randint

class Territory:
	def __init__(self, army=1, owner=""):
		self.armySize = army
		self.owner = owner		
	
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
		assert (1 <= army <= 3) and (army < self.armySize) \
				and (self.owner != defender.owner)
		self.armySize -= army
		
		diceAtk = []
		for i in range(army):
			diceAtk.append(randint(1, 6))
		
		diceDef = []
		for i in range(min(defender.armySize, 3)):
			diceDef.append(randint(1, 6))
		
		diceAtk.sort(reverse=True)
		diceDef.sort(reverse=True)
		
		for df, at in zip(diceDef, diceAtk):
			if df >= at:
				army -= 1
			else:
				defender.armySize -= 1
		
		if defender.armySize == 0:
			defender.setOwner(self.owner)
			defender.reinforce(army)
			conquer = True
		else:
			self.reinforce(army)
			conquer = False
			
		return (conquer, diceAtk, diceDef)
