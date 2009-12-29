import constants

class Territory:
	def __init__(self, owner, numberOfArmies=0):
		if owner in constants.validColors:
			self.owner = owner
		self.numberOfArmies = numberOfArmies
		
	def attack(self, territory, army):
		if not 0 < army <= 3:
			raise Exception("Numero invalido de exercitos.")
		self.owner = ""
		
	def addArmies(self, number):
		self.numberOfArmies += number
	
	def removeArmies(self, number):
		self.numberOfArmies -= number
		if(self.numberOfArmies < 0):
			self.numberOfArmies = 0
