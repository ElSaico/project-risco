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
def join_game(request, name, color, password=None):
	game = _get_obj(name, Game, Error)
	player = game.player_set.filter(user=None)
	if player.count() > 0:
		return False # same as above
	color = game.player_set.filter(color=color)
	if color.count() > 0:
		return False # same as above
	if game.password and password != game.password:
		raise InvalidPasswordError
	Player.objects.create(user=None, game=game, color=color)
	return True

@jsonrpc_method('pyWar.start', authenticated=True)
def start_game(request, name):
	game = _get_obj(name, Game, Error)
	player = game.player_set.filter(user=None)
	if player.count() == 0:
		return False
	game.running = True
	game.save()
	_next_turn(game, player)
	return True

def _next_turn(game, player):
	if player != game.player_set.all()[game.turn_player]: # TODO: shorten it, or encapsulate it.
		raise Error
	# yada yada...
