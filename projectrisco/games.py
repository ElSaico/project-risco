# coding: utf-8
from tornado.web import HTTPError
from tornado.escape import json_encode, json_decode
from pymongo.errors import OperationFailure
from bson.objectid import ObjectId
from formencode import validators
import formencode

from common import RiscoHandler
from boards import Boards

class Games(object):
	def __init__(self, database, user_id):
		self.games = database.game
		self.user = database.user.find_one(user_id)

	def create(self, **parms):
		parms['creator'] = self.user['id']
		parms['board'] = ObjectId(parms['board'])
		return self.games.insert(parms)

	def join(self, game_id, color, password):
		pass

	def public_info(self, game_id):
		pass

class BoardValidator(validators.FancyValidator):
	messages = {
		'invalid_id': u'Não existe mapa com identificador "%(bid)s"',
	}
	def validate_python(self, value, state):
		boards = Boards(state.db)
		if not boards.exists(value): # TODO: early sanity check to see if it's a valid OID
			raise formencode.Invalid(self.message('invalid_id', state, bid=value), value, state)

class CreateForm(formencode.Schema):
	name = validators.String(not_empty=True) # unique
	password = validators.String(if_missing='')
	board = BoardValidator()
	player_objectives = validators.StringBool(if_missing=False)
	global_trade = validators.StringBool(if_missing=False)
	player_color = validators.String(not_empty=True) # VALID_COLORS ou algo assim?

class RESTHandler(RiscoHandler):
	def prepare(self):
		if not self.current_user:
			raise HTTPError(403)
		self.games = Games(self.database, self.current_user['id'])

	def post(self):
		try:
			parms = self.validate(CreateForm)
			new_game = self.games.create(parms)
			self.games.join(new_game, parms["player_color"], parms["password"])
			
			self.set_status(201)
			# TODO: set the Location header to the game's resource URL
			if self.request.headers['Accept'] == 'application/json':
				self.write(self.games.public_info(new_game))
			else:
				self.redirect(self.reverse_url('games'))
		except OperationFailure:
			raise HTTPError(400)
		except formencode.Invalid, e:
			errors = e.unpack_errors()
			if self.request.headers['Accept'] == 'application/json':
				self.set_status(400)
				self.write({'errors': errors})
			else:
				self.set_secure_cookie('errors', json_encode(errors))
				self.set_secure_cookie('form', json_encode(e.value))
				self.redirect(self.reverse_url('game-create'))

class FormHandler(RiscoHandler):
	def prepare(self):
		if not self.current_user:
			raise HTTPError(403)
		self.games = Games(self.database, self.current_user['id'])
		self.boards = Boards(self.database)

	def get(self):
		breadcrumbs = [('Jogos', self.reverse_url('games')), ('Criar jogo', '#')]
		data = self.boards.public_info()
		self.render('game_form.html', breadcrumbs, boards=data['boards'])
