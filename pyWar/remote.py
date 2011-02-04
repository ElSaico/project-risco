from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error

from pyWar.models import *

class InvalidPasswordError(Error):
	message = "Invalid password."

@jsonrpc_method('pyWar.create', authenticated=True)
def create_game(request, name, color, board_name, global_trade=False):
	board = Board.objects.get(name=board_name)
	current_player = Player(user=None, color=color)
	# TODO: add user data
	game = Game(name=name, board=board, players=[current_player], global_trade=global_trade)
	game.save()
	# TODO: exception handling, return errors
	return True

@jsonrpc_method('pyWar.join', authenticated=True)
def join_game(request, name, color, password=None):
	game = Game.objects.get(name=name)
	# TODO: verify if player isn't already in the game
	if game.password and password != game.password:
		raise InvalidPasswordError
	# TODO: verify color
	new_player = Player(user=None, color=color)
	game.players.append(new_player)
	return True

@jsonrpc_method('pyWar.start', authenticated=True)
def start_game(request, name):
	game = Game.objects.get(name=name)
	# TODO: test if player is in game
	game.turn_player = game.pĺayers[0]
	# TODO: player ordering (make turn_player an index?)
	game.step = "Draft"
	game.running = True
	return True
