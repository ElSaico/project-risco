import os
from tornado.ioloop import IOLoop
from tornado.web import Application
from lovely.jsonrpc.dispatcher import JSONRPCDispatcher
from lovely.jsonrpc.tornadohandler import JSONRPCRequestHandler

import remote

application = Application([
	(r"/call", JSONRPCRequestHandler, {'dispatcher': JSONRPCDispatcher(remote.UserAPI())}),
])

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 8888))
	application.listen(port)
	IOLoop.instance().start()
