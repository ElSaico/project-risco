import os
from tornado.ioloop import IOLoop
from tornado.web import Application

import auth
import remote
#import webclient
from common import options

urls = [
	#(r"/", webclient.IndexHandler),
	(r"/login/google", auth.GoogleHandler),
	(r"/resource/user", remote.UserRESTHandler),
	(r"/resource/board", remote.BoardRESTHandler),
	(r"/resource/board/([0-9a-f]+)", remote.BoardRESTHandler),
	(r"/resource/game", remote.GameRESTHandler),
	#(r"/resource/game/([0-9a-f]+)", remote.GameRESTHandler),
]

application = Application(urls, cookie_secret=options.cookie, debug=options.debug)

if __name__ == "__main__":
	application.listen(options.port)
	IOLoop.instance().start()
