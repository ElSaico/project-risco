from tornado.ioloop import IOLoop
from tornado.web import Application

import auth
import remote
import boards
#import webclient
from common import options

urls = [
	#(r"/", webclient.IndexHandler),
	(r"/login/google", auth.GoogleHandler),
	(r"/resource/user", remote.UserRESTHandler),
	(r"/resource/board", boards.BoardRESTHandler),
	(r"/resource/board/([0-9a-f]+)", boards.BoardRESTHandler),
	(r"/resource/game", remote.GameRESTHandler),
	#(r"/resource/game/([0-9a-f]+)", remote.GameRESTHandler),
]

application = Application(urls, cookie_secret=options.cookie, debug=options.debug, database_name=options.database_name)

if __name__ == "__main__":
	application.listen(options.port)
	IOLoop.instance().start()
