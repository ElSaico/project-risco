import os
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import parse_config_file, define, options

#import auth
import remote

define("port", type=int, default=8888)
define("cookie")
parse_config_file("server.conf")

application = Application([
	#(r"/login/google", auth.GoogleHandler),
	(r"/resource/board", remote.BoardRESTHandler),
	(r"/resource/board/([0-9a-f]+)", remote.BoardRESTHandler),
], cookie_secret=options.cookie)

if __name__ == "__main__":
	application.listen(options.port)
	IOLoop.instance().start()