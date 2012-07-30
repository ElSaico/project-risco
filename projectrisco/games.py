from tornado.web import HTTPError
from pymongo.errors import OperationFailure

import models
from common import RiscoHandler

class Games(object):
	def __init__(self, database, user_id):
		self.games = database.game
		self.user = database.user.find_one(user_id)

	def create(self, **parms):
		parms['creator'] = self.user['_id']
		# TODO: transformar parms['board'] em ObjectId
		return self.games.insert(parms)

	def join(self, game_id, color, password):
		pass

	def public_info(self, game_id):
		pass

class GameRESTHandler(RiscoHandler):
	def initialize(self):
		super(GameRESTHandler, self).initialize()
		self.games = Games(self.database, self.current_user['id'])

	def post(self):
		# TODO: descriptive error messages
		if not self.current_user:
			raise HTTPError(403)
		
		POST = self.get_argument
		try:
			new_game = self.games.create(
				name = POST("name"),
				password = POST("password", ""),
				board = POST("board"),
				player_objectives = POST("player_objectives") == 'true',
				global_trade = POST("global_trade") == 'true',
			)
			self.games.join(new_game, POST("player_color"), POST("password"))
		except OperationFailure:
			raise HTTPError(400)
		
		self.set_status(201)
		# TODO: set the Location header to the game's resource URL
		self.write(self.games.public_info(new_game))
