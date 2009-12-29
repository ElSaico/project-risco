import constants

class Territory:
	owner = ""
	numberOfArmies = 0
	def __init__(self, _owner, _numberOfArmies):
		for i in constants.validColors:
			if _owner == i:
				self.owner = _owner

		self.numberOfArmies = _numberOfArmies
		
	def attack(self, _territory):
		self.owner = ""
		
	def addArmies(self, _number):
		self.numberOfArmies += _number
	
	def removeArmies(self, _number):
		self.numberOfArmies -= _number
		if(self.numberOfArmies < 0):
			self.numberOfArmies = 0