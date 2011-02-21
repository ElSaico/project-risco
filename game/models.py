from django.db import models
from django.contrib.auth.models import User

class Territory(models.Model):
	name = models.CharField(max_length=30)
	continent = models.ForeignKey('Continent')
	board = models.ForeignKey('Board')
	borders = models.ManyToManyField('self')
	
	class Meta:
		verbose_name_plural = "territories"
	
	def __unicode__(self):
		return u"%s - %s" % (self.continent, self.name)

class Continent(models.Model):
	name = models.CharField(max_length=30)
	board = models.ForeignKey('Board')
	draft = models.IntegerField()
	
	def __unicode__(self):
		return u"%s - %s" % (self.board, self.name)

class Card(models.Model):
	territory = models.OneToOneField(Territory)
	shape = models.CharField(max_length=20)
	wild_card = models.BooleanField(default=False)
	
	def __unicode__(self):
		if self.wild_card:
			return "Wild card"
		return u"%s card (%s)" % (self.territory, self.shape)

class GameTerritory(models.Model):
	territory = models.ForeignKey(Territory)
	game = models.ForeignKey('Game', related_name="territory_list")
	owner = models.ForeignKey('Player', related_name="territory_list")
	army = models.IntegerField(default=1)
	relocated_army = models.IntegerField(default=0)

class Player(models.Model):
	user = models.ForeignKey(User)
	game = models.ForeignKey('Game')
	cards = models.ManyToManyField(Card)
	color = models.CharField(max_length=10)
	playing = models.BooleanField(default=True)
	draft = models.IntegerField(default=0)
	trade = models.IntegerField(default=0)
	#victory_condition = models.ForeignKey(VictoryCondition)
	
	class Meta:
		ordering = ['?']

class Game(models.Model):
	running = models.BooleanField(default=False)
	name = models.CharField(unique=True, max_length=30)
	password = models.CharField(max_length=20, blank=True)
	board = models.ForeignKey('Board')
	turn = models.IntegerField(default=1)
	turn_player = models.IntegerField(default=0) # an index, to facilitate iteration
	objectives = models.BooleanField()
	global_trade = models.BooleanField()
	step = models.CharField(max_length=10, default="Relocate") # first action is setting to 'Draft'

class Board(models.Model):
	name = models.CharField(unique=True, max_length=30)
	early_trades = models.CommaSeparatedIntegerField(max_length=30)
	late_trades = models.IntegerField()
	
	def __unicode__(self):
		return self.name
