from tornado.ioloop import IOLoop
from tornado.web import Application

import auth
import games
import boards
import users
#import webclient
from common import options

urls = [
	#(r"/", webclient.IndexHandler),
	(r"/login/google", auth.GoogleHandler),
	(r"/resource/user", users.RESTHandler),
	(r"/resource/board", boards.RESTHandler),
	(r"/resource/board/([0-9a-f]+)", boards.RESTHandler),
	(r"/resource/game", games.RESTHandler),
	#(r"/resource/game/([0-9a-f]+)", games.RESTHandler),
]

application = Application(urls, cookie_secret=options.cookie, debug=options.debug, database_name=options.database_name)

if __name__ == "__main__":
	application.listen(options.port)
	IOLoop.instance().start()
