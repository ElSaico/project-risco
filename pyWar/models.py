import mongoengine as db

class Game(db.Document):
	class PlayerTerritory(db.EmbeddedDocument):
		territory = db.ReferenceField(Territory)
		army = db.IntField(default=1, min_length=1)
		relocations = db.IntField(default=0, min_length=0)
	class Player(db.EmbeddedDocument):
		user = db.ReferenceField(User)
		color = db.StringField(unique_with='user')
		territories = db.ListField(db.EmbeddedDocumentField(PlayerTerritory))
		cards = db.ListField(db.ReferenceField(Card))
	players = db.ListField(db.EmbeddedDocumentField(Player))
	board = db.ReferenceField(Board)
	turn = db.IntField(min_value=1)
	turn_player = db.ReferenceField(Player)
	global_trade = db.BooleanField()
	step = db.StringField(regex="[DAR]")

class Board(db.Document): # TODO: implement VictoryCondition as an EmbeddedDocument
	class Territory(db.EmbeddedDocument):
		name = db.StringField()
		borders = db.ListField(db.ReferenceField('self'))
	class Card(db.EmbeddedDocument):
		territory = db.ReferenceField(Territory)
		shape = db.StringField()
		wild_card = db.BooleanField(default=False)
	class Continent(db.EmbeddedDocument):
		territories = db.ListField(db.ReferenceField(Territory))
		bonus = db.IntField()
	name = db.StringField(unique=True)
	colors = db.ListField(db.StringField)
	shapes = db.ListField(db.StringField)
	cards = db.ListField(db.EmbeddedDocumentField(Card))
	continents = db.ListField(db.EmbeddedDocumentField(Continent))
	early_trades = db.ListField(db.IntField)
	late_trades = db.IntField()
