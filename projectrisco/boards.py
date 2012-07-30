import json
from bson.objectid import ObjectId
from tornado.web import HTTPError
from pyvows import Vows, expect
from tornado_pyvows import TornadoHTTPContext

import common

class Boards(object):
	def __init__(self, database):
		self.boards = database.board
		self.territories = database.territory

	def _extract_public_info(self, board):
		board['id'] = str(board['_id'])
		board['num_continents'] = len(board['continents'])
		board['num_territories'] = self.territories.find(
			{'continent': {'$in': board['continents']}}
		).count()
		del board['_id']
		del board['continents']
		del board['cards']
		return board

	def public_info(self, bid=None):
		if bid:
			board = self.boards.find_one(ObjectId(bid))
			if board is None:
				raise Exception # TODO: something more customized
			return self._extract_public_info(board)
		else:
			boards = self.boards.find()
			return {'boards': [self._extract_public_info(board) for board in boards]}

class BoardRESTHandler(common.RiscoHandler):
	def initialize(self):
		super(BoardRESTHandler, self).initialize()
		self.boards = Boards(self.database)

	def get(self, board_id=None):
		try:
			response = self.boards.public_info(board_id)
		except:
			raise HTTPError(404)
		self.write(response)

@Vows.batch
class BoardTest(common.RiscoVows):
	def topic(self):
		common.load_collection_file('tests/test_territories.json', self.database.territory)
		common.load_collection_file('tests/test_continents.json', self.database.continent)
		common.load_collection_file('tests/test_boards.json', self.database.board)
		return Boards(self.database)

	class WhenViewingBoardsByREST(TornadoHTTPContext):
		def topic(self, boards):
			return boards, self.get("/resource/board")

		def should_be_a_valid_resource(self, topic):
			boards, response = topic
			expect(response.code).to_equal(200)

		def should_show_consistent_data(self, topic):
			boards, response = topic
			data = json.loads(response.body)
			expect(data).to_equal(boards.public_info())
