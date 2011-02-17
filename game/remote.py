from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error

from pyWar.models import *

class InvalidPasswordError(Error):
	message = "Invalid password."

def _get_obj(name, cls, error):
	try:
		return cls.objects.get(name=name)
	except Board.DoesNotExist:
		raise e

@jsonrpc_method('pyWar.create', authenticated=True)
def create_game(request, name, password, color, board_name, global_trade=False):
	board = _get_obj(board_name, Board, Error)
	game = Game.objects.create(name=name, password=password,
	                           board=board, global_trade=global_trade)
	Player.objects.create(user=None, game=game, color=color)
	# TODO: add user data
	return True

@jsonrpc_method('pyWar.join', authenticated=True)
def join_game(request, name, color, password=None): # TODO: maximum 6 players! (or Board-defined?)
	game = _get_obj(name, Game, Error)
	player = game.player_set.filter(user=None)
	if player.exists():
		return False # replace with exception
	game_color = game.player_set.filter(color=color)
	if game_color.exists():
		return False # same as above
	if game.password and password != game.password:
		raise InvalidPasswordError
	Player.objects.create(user=None, game=game, color=color)
	return True

@jsonrpc_method('pyWar.start', authenticated=True)
def start_game(request, name): # TODO: minimum 2 players! (or Board-defined?)
	game = _get_obj(name, Game, Error)
	player = game.player_set.filter(user=None)
	if not player.exists():
		return False
	game.running = True
	game.save()
	_set_territory_owners(game)
	_next_step(game, player[0])
	return True

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
		raise Error
	game.step = next_step[game.step]
	if game.step == "Draft":
		for t in player.territory_list.all():
			t.army += t.relocated_army
			t.relocated_army = 0
			t.save()
		game.turn_player = (game.turn_player + 1) % game.player_set.all().count()
		# turning cards goes first?
		_calculate_draft(game, player)
