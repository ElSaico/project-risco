import sys
import os.path
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))

import json
from bson import json_util
from tornado.web import Application
from tornado_pyvows import TornadoHTTPContext
from projectrisco import models
from projectrisco.runserver import urls
from projectrisco.common import options

database_name = options.database_name_test
database = models.c[database_name]

class RiscoVows(TornadoHTTPContext):
	def get_app(self):
		return Application(urls, database=database_name)

def load_collection_file(filename, collection):
	with open(filename) as dump:
		collection.remove()
		data = json.loads(dump.read(), object_hook=json_util.object_hook)
		collection.insert(data)
