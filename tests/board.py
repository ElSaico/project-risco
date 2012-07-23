import json
from pyvows import Vows, expect
from tornado_pyvows import TornadoHTTPContext

import tools

@Vows.batch
class Boards(tools.RiscoVows):
	def topic(self):
		tools.load_collection_file('tests/test_territories.json', tools.database.territory)
		tools.load_collection_file('tests/test_continents.json', tools.database.continent)
		tools.load_collection_file('tests/test_boards.json', tools.database.board)
		return tools.models.Boards(tools.database_name)

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
