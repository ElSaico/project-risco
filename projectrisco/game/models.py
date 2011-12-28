from django.db import models
from django.contrib.auth.models import User

class Territory(models.Model):
	name = models.CharField(max_length=30)
	continent = models.ForeignKey('Continent', related_name='territories')
	board = models.ForeignKey('Board')
	borders = models.ManyToManyField('self')
	
	class Meta:
		verbose_name_plural = "territories"
	
	def __unicode__(self):
		return u"%s - %s" % (self.continent, self.name)

class Continent(models.Model):
	name = models.CharField(max_length=30)
	board = models.ForeignKey('Board', related_name='continents')
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
	game = models.ForeignKey('Game', related_name='players')
	cards = models.ManyToManyField(Card)
	color = models.CharField(max_length=10)
	playing = models.BooleanField(default=True)
	draft = models.IntegerField(default=0)
	trade = models.IntegerField(default=0)
	#victory_condition = models.ForeignKey(VictoryCondition)
	
	class Meta:
		ordering = ['?']
	
	def calculate_draft(self):
		# TODO: add continental bonus (GameContinent?)
		self.draft = self.territory_list.count() / 2
		self.save()

class Game(models.Model):
	running = models.BooleanField(default=False)
	name = models.CharField(unique=True, max_length=30)
	password = models.CharField(max_length=20, blank=True)
	board = models.ForeignKey('Board')
	turn = models.IntegerField(default=1)
	_turn_player = models.IntegerField(default=0)
	objectives = models.BooleanField()
	global_trade = models.BooleanField()
	step = models.CharField(max_length=10, default="Relocate") # first action is setting to 'Draft'
	
	def start(self):
		self.running = True
		territories = self.board.territory_set.order_by('?')
		i = 0
		for ter in territories:
			players = self.player_set.all()
			GameTerritory.objects.create(game=self, territory=ter, owner=players[i])
			i = (i+1) % players.count()
		self.save()
		self.next_step(players[0])
	
	def next_step(self, player):
		_next_step = {'Draft': 'Attack', 'Attack': 'Relocate', 'Relocate': 'Draft'}
		if player != self.turn_player():
			raise Exception, "Turn is for another player"
		self.step = _next_step[self.step]
		if self.step == "Draft":
			for t in player.territory_list.all():
				t.army += t.relocated_army
				t.relocated_army = 0
				t.save()
			while not self.turn_player().playing:
				self._turn_player = (self._turn_player + 1) % self.player_set.count()
			self.save()
			# turning cards goes first?
			self.calculate_draft(player)
	
	def turn_player(self):
		return self.player_set.all()[self._turn_player]

class Board(models.Model):
	name = models.CharField(unique=True, max_length=30)
	min_players = models.IntegerField()
	max_players = models.IntegerField()
	early_trades = models.CommaSeparatedIntegerField(max_length=30)
	late_trades = models.IntegerField()
	
	def __unicode__(self):
		return self.name
