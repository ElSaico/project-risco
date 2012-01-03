from django.core.urlresolvers import reverse
from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error

from game.models import *

def _get_obj(name, cls, error_msg):
	try:
		return cls.objects.get(name=name)
	except cls.DoesNotExist:
		raise Error, error_msg

@jsonrpc_method('user.status')
def user_data(request):
	response = {'logged': request.user.is_authenticated()}
	if not response['logged']:
		response['login_url'] = {backend.title(): reverse('socialauth_login', args=[backend])
		                         for backend in ('twitter', 'facebook', 'google', 'yahoo')}
	else:
		response['logout_url'] = reverse('logout')
	return response

@jsonrpc_method('game.list')
def list_games(request, with_user=False, filters={}):
	games = Game.objects.filter(**filters)
	if with_user:
		games = games.filter(players__user=request.user)
	return [ {"name": game.name,
	         "board": str(game.board),
	   "num_players": game.players.count(),
	  "has_password": bool(game.password),
	  "global_trade": game.global_trade,
	    "objectives": game.objectives,
	       "running": game.running,
	         } for game in games ]
	
@jsonrpc_method('game.create', authenticated=True)
def create_game(request, game_name, game_password, board_name, objectives, global_trade, player_color):
	if objectives:
		raise Error, "Objectives not implemented yet"
	board = _get_obj(board_name, Board, "Board doesn't exist")
	game = Game.objects.create(name=game_name, password=game_password, board=board,
	                           objectives=objectives, global_trade=global_trade)
	Player.objects.create(user=request.user, game=game, color=player_color)

@jsonrpc_method('game.join', authenticated=True)
def join_game(request, color, game_name, game_password):
	game = _get_obj(game_name, Game, "Game doesn't exist")
	if game.running:
		raise Error, "Game is already running"
	player = game.players.filter(user=request.user)
	if player.exists():
		raise Error, "Player already in game"
	if game.players.count() >= game.board.max_players:
		raise Error, "Limit of players reached"
	game_color = game.players.filter(color=color)
	if game_color.exists():
		raise Error, "Color already in use"
	if game.password and game_password != game.password:
		raise Error, "Invalid password"
	Player.objects.create(user=request.user, game=game, color=color)

@jsonrpc_method('game.start', authenticated=True)
def start_game(request, game_name):
	game = _get_obj(game_name, Game, "Game doesn't exist")
	if game.running:
		raise Error, "Game is already running"
	player = game.players.filter(user=request.user)
	if not player.exists():
		raise Error, "Player not in game"
	if game.players.count() < game.board.min_players:
		raise Error, "Too few players"
	try:
		game.start()
	except Exception, msg:
		return Error, msg
