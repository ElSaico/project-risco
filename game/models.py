from django.db import models

class Territory(models.Model):
	name = models.CharField(max_length=30)
	continent = models.ForeignKey(Continent)
	board = models.ForeignKey(Board)
	borders = models.ManyToManyField('self')

class Continent(models.Model):
	name = models.CharField(max_length=30)
	draft = models.IntegerField()

class Card(models.Model):
	territory = models.OneToOneField(Territory)
	shape = models.CharField(max_length=20)
	wild_card = models.BooleanField(default=False)

class GameTerritory(models.Model):
	territory = models.ForeignKey(Territory)
	game = models.ForeignKey(Game, related_name="territory_list")
	owner = models.ForeignKey(Player, related_name="territory_list")
	army = models.IntegerField(default=1)
	relocated_army = models.IntegerField(default=0)

class Player(models.Model):
	user = models.ForeignKey(User)
	game = models.ForeignKey(Game)
	cards = models.ManyToManyField(Card)
	color = models.CharField(max_length=10)
	playing = models.BooleanField(default=True)
	draft = models.IntegerField()
	#victory_condition = models.ForeignKey(VictoryCondition)

class Game(models.Model):
	running = models.BooleanField(default=False)
	name = models.CharField(unique=True, max_length=30)
	password = models.CharField(min_length=4)
	board = models.ForeignKey(Board)
	turn = models.IntegerField(default=1)
	turn_player = models.IntegerField(default=0) # an index, to facilitate iteration
	global_trade = models.BooleanField()
	step = models.CharField(max_length=10)

class Board(models.Model):
	name = models.StringField(unique=True)
	early_trades = models.CommaSeparatedIntegerField(max_length=30)
	late_trades = models.IntegerField()
