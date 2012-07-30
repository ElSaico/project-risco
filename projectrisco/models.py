# TODO: create 'bootstrap' file with database indexes, etc.

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
