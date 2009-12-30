import constants

class Territory:
	def __init__(self, owner, numberOfArmies=0):
		self.setOwner(owner)
		self.setNumberOfArmies(numberOfArmies)
		
	def setOwner(self, owner):
		if owner in constants.validColors:
			self.owner = owner
		else:
			raise Exception("Invalid territory owner.")
	
	def setNumberOfArmies(self, number):
		if number < 0:
			self.numberOfArmies = 0
		else:
			self.numberOfArmes = number
	
	def addArmies(self, number):
		self.setNumberOfArmies(numberOfArmies + number)
	
	def removeArmies(self, number):
		self.setNumberOfArmies(numberOfArmies - number)

	def attack(self, territory, army):
		if (not 0 < army <= 3) or (army > self.numberOfArmies):
			raise Exception("Invalid number of armies.")
		#attack action here