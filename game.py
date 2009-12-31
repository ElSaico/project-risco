class Game:
	def __init__(self):
		self.players = []
		self.worldmap = None
		
	def addPlayer(self, player):
		if not player in self.players:
			self.players.append(player)
	
	def start(self):
		self.worldmap = Map(self.players)
		# game action here