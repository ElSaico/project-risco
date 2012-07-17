import pymongo
from bson.objectid import ObjectId

from common import options

c = pymongo.Connection(options.database_uri)

# TODO: add 'bootstrap' file with indexes, etc.
class RiscoCollection(object):
	def __init__(self, database=options.database_name):
		self.database = c[database]
		self.collection = c[database][self.collection_name]

class Boards(RiscoCollection):
	collection_name = 'board'

	def _extract_public_info(self, board):
		board['id'] = str(board['_id'])
		del board['_id']
		board['num_continents'] = len(board['continents'])
		board['num_territories'] = self.database.territory.find(
			{'continent': {'$in': board['continents']}}
		).count()
		del board['continents']
		return board

	def public_info(self, bid=None):
		if bid:
			board = self.collection.find_one(ObjectId(bid))
			if board is None:
				raise Exception # TODO: something more customized
			return self._extract_public_info(board)
		else:
			boards = self.collection.find()
			return {'boards': [self._extract_public_info(board) for board in boards]}

#class GoogleUser(User):
#	email = StringField(unique=True)
#	name = StringField()
#	first_name = StringField()
#	last_name = StringField()
#	locale = StringField()

#class PlayerArmy(EmbeddedDocument):
#	territory = ReferenceField(Territory)
#	soldiers = IntField()

#class Player(Document):
#	user = ReferenceField(User)
#	cards = ListField(ReferenceField(Card))
#	color = StringField() # needs restrictions
#	playing = BooleanField(default=True)
#	trade = IntField(default=0)
#	armies = ListField(EmbeddedDocumentField(PlayerArmy))

#class Game(Document):
#	board = ReferenceField(Board)
#	name = StringField(unique=True, required=True)
#	password = StringField()
#	creator = ReferenceField(User, required=True)
#	players = ListField(ReferenceField(Player))
#	player_objectives = BooleanField(required=True)
#	global_trade = BooleanField(required=True)
#	round = IntField(default=0)
#	current_player = ObjectIdField()
#	turn_step = IntField(default=0)
#	running = BooleanField(default=False)
#	finished = BooleanField(default=False)
#	winner = ReferenceField(Player)
