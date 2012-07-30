from tornado.web import HTTPError

import models
from common import RiscoHandler

class UserRESTHandler(RiscoHandler):
	def get(self):
		response = {'logged': bool(self.current_user)}
		if response['logged']:
			response['user'] = self.current_user
		self.write(response)

class GameRESTHandler(RiscoHandler):
	def post(self):
		# TODO: descriptive error messages
		if not self.current_user:
			raise HTTPError(403)
		
		POST = self.get_argument
		user = models.User(id=self.current_user['id'])
		try:
			new_game = models.Game.create(
				name = POST("name"),
				password = POST("password", ""),
				board = POST("board"),
				player_objectives = POST("player_objectives") == 'true',
				global_trade = POST("global_trade") == 'true',
				creator = user,
			)
			new_game.new_player(user, POST("player_color"), POST("password"))
		except ValidationError:
			raise HTTPError(400)
		
		self.set_status(201)
		# TODO: set the Location header to the game's resource URL
		self.write(new_game.public_info())
