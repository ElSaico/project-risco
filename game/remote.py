from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error

from game.models import *

def _get_obj(name, cls, error_msg):
	try:
		return cls.objects.get(name=name)
	except cls.DoesNotExist:
		raise Error, error_msg

@jsonrpc_method('pyWar.create', authenticated=True)
def create_game(request, game_name, game_password, board_name, global_trade, color):
	board = _get_obj(board_name, Board, "Board doesn't exist")
	game = Game.objects.create(name=game_name, password=game_password,
	                           board=board, global_trade=global_trade)
	Player.objects.create(user=request.user, game=game, color=color)

@jsonrpc_method('pyWar.join', authenticated=True)
def join_game(request, color, game_name, game_password): # TODO: maximum 6 players! (or Board-defined?)
	game = _get_obj(game_name, Game, "Game doesn't exist")
	player = game.player_set.filter(user=request.user)
	if player.exists():
		raise Error, "Player already in game"
	game_color = game.player_set.filter(color=color)
	if game_color.exists():
		raise Error, "Color already in use"
	if game.password and game_password != game.password:
		raise Error, "Invalid password"
	Player.objects.create(user=request.user, game=game, color=color)

@jsonrpc_method('pyWar.start', authenticated=True)
def start_game(request, game_name): # TODO: minimum 2 players! (or Board-defined?)
	game = _get_obj(game_name, Game, "Game doesn't exist")
	player = game.player_set.filter(user=request.user)
	if not player.exists():
		raise Error, "Player not in game"
	game.running = True
	game.save()
	_set_territory_owners(game)
	_next_step(game, player[0])

def _set_territory_owners(game):
	territories = game.board.territory_set.order_by('?')
	i = 0
	for ter in territories:
		players = game.player_set.all()
		GameTerritory.objects.create(game=game, territory=ter, owner=players[i])
		i = (i+1) % players.count()

def _next_step(game, player):
	next_step = {'Draft': 'Attack', 'Attack': 'Relocate', 'Relocate': 'Draft'}
	if player != game.player_set.all()[game.turn_player]: # TODO: shorten it, or encapsulate it.
		raise Error, "Turn is for another player"
	game.step = next_step[game.step]
	if game.step == "Draft":
		for t in player.territory_list.all():
			t.army += t.relocated_army
			t.relocated_army = 0
			t.save()
		game.turn_player = (game.turn_player + 1) % game.player_set.all().count()
		# turning cards goes first?
		_calculate_draft(game, player)
