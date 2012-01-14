from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode

import models

class BoardRESTHandler(RequestHandler):
	def get(self, board_id=None):
		if board_id:
			try:
				response = models.Board.objects(_id=board_id)[0].public_info()
			except KeyError:
				raise HTTPError(404)
		else:
			response = [b.public_info() for b in models.Board.objects]
		self.set_header("Content-Type", "application/json")
		self.write(json_encode(response))
