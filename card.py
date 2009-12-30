import constants

class Card:
	def __init__(self, name, shape):
		assert shape in constants.validShapes
		self.shape = shape
		assert name in constants.territories
		this.name = name