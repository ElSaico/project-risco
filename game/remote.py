from jsonrpc import jsonrpc_method
from jsonrpc.exceptions import Error

from game.models import *

def _get_obj(name, cls, error_msg):
	try:
		return cls.objects.get(name=name)
	except cls.DoesNotExist:
		raise Error, error_msg

@jsonrpc_method('pyWar.games')
def list_games(request, filters=None):
	if filters:
		games = Game.objects.filter(**filters)
	else:
		games = Game.objects.all()
	return [ {"name": game.name,
	         "board": str(game.board),
	   "num_players": game.player_set.count(),
	  "has_password": bool(game.password),
	  "global_trade": game.global_trade,
	    "objectives": game.objectives,
	       "running": game.running,
	         } for game in games ]

@jsonrpc_method('pyWar.userGames', authenticated=True)
def user_games(request):
	user_players = Player.objects.filter(user=request.user)
	return [ {"name": p.game.name,
	         "board": str(p.game.board),
	   "num_players": p.game.player_set.count(),
	  "has_password": bool(p.game.password),
	  "global_trade": p.game.global_trade,
	    "objectives": p.game.objectives,
	       "running": p.game.running,
	         } for p in user_players ]
	
@jsonrpc_method('pyWar.create', authenticated=True)
def create_game(request, game_name, game_password, board_name, objectives, global_trade, player_color):
	if objectives:
		raise Error, "Objectives not implemented yet"
	board = _get_obj(board_name, Board, "Board doesn't exist")
	game = Game.objects.create(name=game_name, password=game_password, board=board,
	                           objectives=objectives, global_trade=global_trade)
	Player.objects.create(user=request.user, game=game, color=player_color)

@jsonrpc_method('pyWar.join', authenticated=True)
def join_game(request, color, game_name, game_password):
	game = _get_obj(game_name, Game, "Game doesn't exist")
	if game.running:
		raise Error, "Game is already running"
	player = game.player_set.filter(user=request.user)
	if player.exists():
		raise Error, "Player already in game"
	if game.player_set.count() >= game.board.max_players:
		raise Error, "Limit of players reached"
	game_color = game.player_set.filter(color=color)
	if game_color.exists():
		raise Error, "Color already in use"
	if game.password and game_password != game.password:
		raise Error, "Invalid password"
	Player.objects.create(user=request.user, game=game, color=color)

@jsonrpc_method('pyWar.start', authenticated=True)
def start_game(request, game_name):
	game = _get_obj(game_name, Game, "Game doesn't exist")
	if game.running:
		raise Error, "Game is already running"
	player = game.player_set.filter(user=request.user)
	if not player.exists():
		raise Error, "Player not in game"
	if game.player_set.count() < game.board.min_players:
		raise Error, "Too few players"
	try:
		game.start()
	except Exception, msg:
		return Error, msg
