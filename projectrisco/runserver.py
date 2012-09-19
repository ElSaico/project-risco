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
	url(r"/boards", boards.RESTHandler, name='boards'),
	url(r"/boards/([0-9a-f]+)", boards.RESTHandler, name='board'),
	url(r"/games", games.RESTHandler, name='games'),
	url(r"/games/([0-9a-f]+)", games.RESTHandler, name='game'),
	url(r"/games/new", games.FormHandler, name='game-create'),
	url(r"/login/google", auth.GoogleHandler, name='google'),
	url(r"/logout", auth.LogoutHandler, name='logout'),
	url(r"/user", users.RESTHandler, name='current-user'),
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
