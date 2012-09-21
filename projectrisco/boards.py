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

	def exists(self, bid):
		res = self.boards.find({'_id': ObjectId(bid)})
		return res.count() > 0

	def public_info(self, bid=None):
		if bid:
			board = self.boards.find_one(ObjectId(bid))
			if board is None:
				raise Exception # TODO: something more customized
			return self._extract_public_info(board)
		else:
			boards = self.boards.find()
			return {'boards': [self._extract_public_info(board) for board in boards]}

class RESTHandler(common.RiscoHandler):
	def initialize(self):
		super(RESTHandler, self).initialize()
		self.boards = Boards(self.database)

	def get(self, board_id=None):
		try:
			data = self.boards.public_info(board_id)
		except:
			raise HTTPError(404)
		
		if self.request.headers['Accept'] == 'application/json':
			self.write(data)
		else:
			breadcrumbs = [('Mapas', self.reverse_url('boards'))]
			if board_id:
				breadcrumbs.append((data['name'], self.reverse_url('board', data['id'])))
				self.render('board.html', breadcrumbs, board=data)
			else:
				self.render('boards.html', breadcrumbs, boards=data['boards'])

@Vows.batch
class BoardTest(common.RiscoVows):
	def topic(self):
		common.load_collection_file('tests/test_territories.json', self.database.territory)
		common.load_collection_file('tests/test_continents.json', self.database.continent)
		boards = common.load_collection_file('tests/test_boards.json', self.database.board)
		return boards, Boards(self.database)

	class WhenViewingBoardsByREST(TornadoHTTPContext):
		def topic(self, topic):
			data, boards = topic
			return data, boards, self.get("/resource/board")

		def should_be_a_valid_resource(self, topic):
			data, boards, response = topic
			expect(response.code).to_equal(200)

		def should_show_consistent_data(self, topic):
			data, boards, response = topic
			response_data = json.loads(response.body)
			expect(response_data).to_equal(boards.public_info())

		def should_show_correct_amount(self, topic):
			data, boards, response = topic
			response_data = json.loads(response.body)
			expect(response_data['boards']).to_length(len(data))

	class WhenViewingABoardByREST(TornadoHTTPContext):
		def topic(self, topic):
			data, boards = topic
			board = data[0]
			board['_id'] = str(board['_id'])
			return board, boards, self.get("/resource/board/"+board['_id'])

		def should_be_a_valid_resource(self, topic):
			data, boards, response = topic
			expect(response.code).to_equal(200)

		def should_show_consistent_data(self, topic):
			data, boards, response = topic
			response_data = json.loads(response.body)
			expect(response_data).to_equal(boards.public_info(data['_id']))

		def should_show_correct_fields(self, topic):
			data, boards, response = topic
			response_data = json.loads(response.body)
			expect(response_data).to_include('id')
			expect(response_data).to_include('name')
			expect(response_data).to_include('min_players')
			expect(response_data).to_include('max_players')
			expect(response_data).to_include('num_continents')
			expect(response_data).to_include('num_territories')
			expect(response_data).to_include('early_trades')
			expect(response_data).to_include('late_trades')
