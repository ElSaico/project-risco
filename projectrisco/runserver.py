from tornado.ioloop import IOLoop
from tornado.web import Application
from lovely.jsonrpc.dispatcher import JSONRPCDispatcher
from lovely.jsonrpc.tornadohandler import JSONRPCRequestHandler

import remote

SERVER_PORT = 8888

application = Application([
	(r"/call", JSONRPCRequestHandler, {'dispatcher': JSONRPCDispatcher(remote.UserAPI())}),
])

if __name__ == "__main__":
	application.listen(SERVER_PORT)
	IOLoop.instance().start()
