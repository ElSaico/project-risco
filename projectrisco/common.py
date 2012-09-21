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

	def validate(self, validator):
		class State(object):
			db = self.database
		args = dict([(field, values[-1]) for field, values in self.request.arguments.iteritems()])
		return validator.to_python(args, state=State())

	def render(self, template_name, breadcrumbs=None, **vars):
		errors = self.get_secure_cookie('errors') or '{}'
		self.clear_cookie('errors')
		vars['errors'] = json_decode(errors)
		form = self.get_secure_cookie('form') or '{}'
		self.clear_cookie('form')
		vars['form'] = json_decode(form)
		if breadcrumbs:
			vars['breadcrumbs'] = [('Home', '/')] + breadcrumbs
		template = self.templates.get_template(template_name)
		self.write(template.render(**vars))

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
