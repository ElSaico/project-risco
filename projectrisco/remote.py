from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode, json_decode
from mongoengine import ValidationError

import models

class RESTHandler(RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("auth")

class BoardRESTHandler(RESTHandler):
	def get(self, board_id=None):
		if board_id:
			try:
				response = models.Board.objects.get(id=board_id).public_info()
			except ValidationError:
				raise HTTPError(404)
		else:
			response = [b.public_info() for b in models.Board.objects]
		self.set_header("Content-Type", "application/json")
		self.write(json_encode(response))

class UserRESTHandler(RESTHandler):
	def get(self):
		response = {'logged': bool(self.current_user)}
		if response['logged']:
			response['user'] = json_decode(self.current_user)
		self.set_header("Content-Type", "application/json")
		self.write(json_encode(response))
