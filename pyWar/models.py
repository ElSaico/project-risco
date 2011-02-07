import mongoengine as db

class Territory(db.EmbeddedDocument):
	name = db.StringField()
	borders = db.ListField(db.ReferenceField('self'))

class Continent(db.EmbeddedDocument):
	name = db.StringField()
	territories = db.ListField(db.ReferenceField(Territory))
	bonus = db.IntField()

class Card(db.EmbeddedDocument):
	territory = db.ReferenceField(Territory)
	shape = db.StringField()
	wild_card = db.BooleanField(default=False)

class PlayerTerritory(db.EmbeddedDocument):
	territory = db.ReferenceField(Territory)
	army = db.IntField(default=1, min_length=1)
	relocations = db.IntField(default=0, min_length=0)

class Player(db.EmbeddedDocument):
	user = db.ReferenceField(User)
	game = db.ReferenceField(Game) # backreference needed to fetch some info
	color = db.StringField()
	playing = db.BooleanField(default=True)
	territories = db.ListField(db.EmbeddedDocumentField(PlayerTerritory), default=[])
	cards = db.ListField(db.ReferenceField(Card), default=[])
	draft = db.IntField()
	victory_condition = db.DictField()

class Game(db.Document):
	running = db.BooleanField(default=False)
	name = db.StringField(unique=True)
	password = db.StringField(min_length=4)
	players = db.ListField(db.EmbeddedDocumentField(Player))
	board = db.ReferenceField(Board)
	turn = db.IntField(min_value=1)
	turn_player = db.ReferenceField(Player)
	global_trade = db.BooleanField()
	step = db.StringField(regex="[DAR]")

class Board(db.Document):
	name = db.StringField(unique=True)
	colors = db.ListField(db.StringField())
	shapes = db.ListField(db.StringField())
	cards = db.ListField(db.EmbeddedDocumentField(Card))
	continents = db.ListField(db.EmbeddedDocumentField(Continent))
	early_trades = db.ListField(db.IntField())
	late_trades = db.IntField()
	victory_conditions = db.ListField(db.DictField()) # very loose structure
