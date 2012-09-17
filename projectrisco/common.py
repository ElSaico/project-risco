import pymongo
import json
from bson import json_util
from tornado.web import Application, RequestHandler
from tornado.options import parse_config_file, define, options
from tornado.escape import json_decode
from tornado_pyvows import TornadoHTTPContext
from jinja2 import Environment, FileSystemLoader

define("debug", type=bool, default=True)
define("port", type=int, default=8888)
define("cookie")
define("database_name", default="risco")
define("database_uri", default="mongodb://localhost/risco")
define("database_name_test", default="risco-test")
define("database_uri_test", default="mongodb://localhost/risco-test")
parse_config_file("server.conf")

class RiscoHandler(RequestHandler):
	def initialize(self, collection_name=None):
		connection = pymongo.Connection(options.database_uri)
		self.database = connection[self.settings['database_name']]
		self.templates = Environment(loader=FileSystemLoader('templates/'))
		for attr in ('reverse_url', 'static_url', 'current_user'):
			self.templates.globals[attr] = getattr(self, attr)
		if collection_name:
			self.collection = self.database[collection_name]

	def get_current_user(self):
		data = self.get_secure_cookie("auth")
		if data:
			return json_decode(data)
		else:
			return data

class RiscoVows(TornadoHTTPContext):
	database = pymongo.Connection(options.database_uri)[options.database_name_test]
	def get_app(self):
		from runserver import urls
		return Application(urls, database_name=options.database_name_test)

def load_collection_file(filename, collection):
	with open(filename) as dump:
		collection.remove()
		data = json.loads(dump.read(), object_hook=json_util.object_hook)
		collection.insert(data)
		return data
