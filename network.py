#import bz2
import socket
from communication.communication_pb2 import ClientToServer, ServerToClient

class Client:
	BUFSIZE = 16384
	DEBUG = True
	
	def __init__(self, ip, port, color):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect((ip, port))
		cts = ClientToServer()
		assert not cts.HasField("player_info")
		cts.player_info.color = color
		assert cts.HasField("player_info")
		self.client.send(cts.SerializeToString())
	
	def receiveMap(self):
		data = self.client.recv(self.BUFSIZE)
		while not data:
			data = self.client.recv(self.BUFSIZE)
		self.stc = ServerToClient()
		self.stc.ParseFromString(data)
		assert self.stc.HasField("map_info") and self.stc.HasField("turn_info")
	
	def map(self):
		#return bz2.decompress(stc.map_info)
		return self.stc.map_info
	
	def players(self):
		return self.stc.players
	
	def turn(self):
		return self.stc.turn_info.player
	
	def step(self):
		return self.stc.turn_info.step

class Server:
	BUFSIZE = 16384
	DEBUG = True
	
	def __init__(self, port):
		self._clients = {}
		self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._server.bind(("", port))
		#self._server.bind((socket.gethostname(), port))
		self._server.listen(2)
		self._server.settimeout(0.0)
	
	def listen(self):
		try:
			client, addr = self._server.accept()
			if client:
				client.settimeout(0.5)
				data = client.recv(self.BUFSIZE)
				while not data:
					data = client.recv(self.BUFSIZE)
				
				cts = ClientToServer()
				cts.ParseFromString(data)
				if cts.HasField("player_info"):
					playing = False
					for c in self._clients:
						if c[IP] == addr[0] or c[COLOR] == cts.player_info.color:
							playing = True
							print "Refused connection from:", cts.player_info.color, addr[0]
					# also need to check if the received color is different from self color
					# and if the received color is valid
					if not playing:
						print cts.player_info.color, "connected from", addr[0]
						self._clients[cts.player_info.color] = (client, addr[0])
						return addr[0], cts.player_info.color
		except:
			pass
		return None, None
	
	def sendMap(self, game):
		self._game = game
		stc = ServerToClient()
		#stc.map_info = bz2.compress(self._game.worldmap.toClient())
		stc.map_info = self._game.worldmap.toClient()
		for c in self._clients.keys():
			stc.players.colors.append(c)
		stc.turn_info.player = self._game.turn
		stc.turn_info.step = self._game.step
		if self.DEBUG:
			print "Map size: ", len(stc.map_info)
		for c, ip in self._clients.values():
			c.send(stc.SerializeToString())
	
	def clients(self):
		return self._clients.keys()
