from mongoengine import *

connect('risco')

class Board(Document):
	name = StringField(unique=True)
	min_players = IntField()
	max_players = IntField()
	early_trades = ListField(IntField())
	late_trades = IntField()
	continents = ListField(ReferenceField('Continent'))
	cards = ListField(ReferenceField('Card'))
	meta = {'indexes': ['name']}

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
