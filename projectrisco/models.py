import os
from pymongo.uri_parser import parse_uri
from mongoengine import *

uri = parse_uri(os.environ.get('MONGOLAB_URI', 'mongodb://localhost/risco'))
connect(uri['database'], uri['username'], uri['password'],
        host=uri['nodelist'][0][0], port=uri['nodelist'][0][1])

class Board(Document):
	meta = {'indexes': ['name']}
	
	name = StringField(unique=True)
	min_players = IntField()
	max_players = IntField()
	early_trades = ListField(IntField())
	late_trades = IntField()
	continents = ListField(ReferenceField('Continent'))
	cards = ListField(ReferenceField('Card'))
	
	def public_info(self):
		return {
			'id': str(self._id),
			'name': self.name,
			'min_players': self.min_players,
			'max_players': self.max_players,
			'num_continents': len(self.continents),
			'num_territories': sum([len(c.territories) for c in self.continents]),
		}

class Continent(Document):
	name = StringField(unique=True)
	draft = IntField()
	territories = ListField(ReferenceField('Territory'))
	meta = {'indexes': ['name']}

class Territory(Document):
	name = StringField(unique=True)
	borders = ListField(ReferenceField('self'))
	meta = {'indexes': ['name']}

class Card(Document):
	territory = ReferenceField(Territory)
	shape = StringField(choices=('Any', 'Square', 'Triangle', 'Circle'))

class User(Document):
	pass

class GoogleUser(User):
	email = StringField(unique=True)
	name = StringField()
	first_name = StringField()
	last_name = StringField()
	locale = StringField()

class PlayerArmy(EmbeddedDocument):
	territory = ReferenceField(Territory)
	soldiers = IntField()

class Player(Document):
	user = ReferenceField(User)
	cards = ListField(ReferenceField(Card))
	color = StringField() # needs restrictions
	playing = BooleanField(default=True)
	trade = IntField(default=0)
	armies = ListField(EmbeddedDocumentField(PlayerArmy))

class Game(Document):
	board = ReferenceField(Board)
	name = StringField(unique=True, required=True)
	password = StringField()
	creator = ReferenceField(User, required=True)
	players = ListField(ReferenceField(Player))
	player_objectives = BooleanField(required=True)
	global_trade = BooleanField(required=True)
	round = IntField(default=0)
	current_player = ObjectIdField()
	turn_step = IntField(default=0)
	running = BooleanField(default=False)
	finished = BooleanField(default=False)
	winner = ReferenceField(Player)
