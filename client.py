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
