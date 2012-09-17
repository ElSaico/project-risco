from tornado.ioloop import IOLoop
from tornado.web import Application, url

import auth
import games
import boards
import users
#import webclient
from common import options

urls = [
	#url(r"/", webclient.IndexHandler, name='index'),
	url(r"/boards", boards.HTMLHandler, name='boards'),
	url(r"/boards/([0-9a-f]+)", boards.HTMLHandler, name='board'),
	url(r"/login/google", auth.GoogleHandler, name='google'),
	url(r"/logout", auth.LogoutHandler, name='logout'),
	(r"/resource/user", users.RESTHandler),
	(r"/resource/board", boards.RESTHandler),
	(r"/resource/board/([0-9a-f]+)", boards.RESTHandler),
	(r"/resource/game", games.RESTHandler),
	#(r"/resource/game/([0-9a-f]+)", games.RESTHandler),
]

application = Application(urls,
	cookie_secret=options.cookie,
	debug=options.debug,
	database_name=options.database_name,
	template_path='templates/',
	static_path='static/'
)

if __name__ == "__main__":
	application.listen(options.port)
	IOLoop.instance().start()
