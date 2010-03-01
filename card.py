class Card:
	def __init__(self, name=None, shape=None, **kwargs):
		if "wild" in kwargs:
			self.wild = kwargs["wild"]
		else:
			self.wild = False
		self.shape = shape
		self.name = name
	
	def __str__(self):
		if self.wild:
			return "Wild card"
		else:
			return "{0} ({1})".format(self.name, self.shape)
	
	@staticmethod
	def match(c): # not tested yet
		assert len(c) == 3
		cards = filter(lambda x: not x.wild, c)
		if len(cards) <= 2:
			return True
		else:
			return cards[0].shape == cards[1].shape == cards[2].shape or \
			       cards[0].shape != cards[1].shape != cards[2].shape
