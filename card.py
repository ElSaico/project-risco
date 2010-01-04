import constants

class Card:
	def __init__(self, name, shape):
		assert shape in constants.validShapes
		self.shape = shape
		#assert name in constants.territories
		self.name = name
	
	def __str__(self):
		return "%s (%s)" % (self.name, self.shape)
