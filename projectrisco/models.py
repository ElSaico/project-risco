from mongoengine import *

connect('risco')

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
