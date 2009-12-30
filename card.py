class Card:
	def __init__(self, name, shape):
		if shape in constants.validShapes:
			self.shape = shape
		else:
			raise Exception("Invalid shape.")
		this.name = name