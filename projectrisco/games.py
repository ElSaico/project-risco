# coding: utf-8
from tornado.web import HTTPError
from tornado.escape import json_encode, json_decode
from pymongo.errors import OperationFailure
from bson.dbref import DBRef
from bson.objectid import ObjectId
from formencode import validators
import formencode

from common import RiscoHandler
from boards import Boards

class Games(object):
	def __init__(self, database, user_id):
		self.db = database
		self.user = database.user.find_one(ObjectId(user_id))

	def create(self, **parms):
		parms['creator'] = DBRef('user', self.user['_id'])
		parms['board'] = DBRef('board', ObjectId(parms['board']))
		return self.db.game.insert(parms)

	def has_name(self, name):
		res = self.db.game.find({'name': name})
		return res.count() > 0

	def join(self, game_id):
		player = {
			'user': DBRef('user', self.user['_id']),
			'game': DBRef('game', ObjectId(game_id)),
		}
		return self.db.player.insert(player)

	def public_info(self, game_id):
		pass

class NameValidator(validators.FancyValidator):
	messages = {
		'name_exists': u'Já existe um mapa com o nome "%(name)s"',
	}
	def validate_python(self, value, state):
		games = Games(state.db, state.user['id'])
		if games.has_name(value):
			raise formencode.Invalid(self.message('name_exists', state, name=value), value, state)

class BoardValidator(validators.FancyValidator):
	messages = {
		'invalid_id': u'Não existe mapa com identificador "%(bid)s"',
	}
	def validate_python(self, value, state):
		boards = Boards(state.db)
		if not boards.exists(value): # TODO: early sanity check to see if it's a valid OID
			raise formencode.Invalid(self.message('invalid_id', state, bid=value), value, state)

class CreateForm(formencode.Schema):
	name = NameValidator()
	password = validators.String(if_missing='')
	board = BoardValidator()
	player_objectives = validators.StringBool(if_missing=False)
	global_trade = validators.StringBool(if_missing=False)

class RESTHandler(RiscoHandler):
	def prepare(self):
		if not self.current_user:
			raise HTTPError(403)
		self.games = Games(self.database, self.current_user['id'])

	def post(self):
		try:
			parms = self.validate(CreateForm)
			new_game = self.games.create(**parms)
			self.games.join(new_game)
			
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
