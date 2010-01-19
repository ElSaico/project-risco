class Card:
	validShapes = ("Circle", "Square", "Triangle")
	
	def __init__(self, name, shape):
		assert shape in self.validShapes
		self.shape = shape
		#assert name in constants.territories
		self.name = name
	
	def __str__(self):
		return "{0} ({1})".format(self.name, self.shape)
