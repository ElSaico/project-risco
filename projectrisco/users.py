from common import RiscoHandler

class UserRESTHandler(RiscoHandler):
	def get(self):
		response = {'logged': bool(self.current_user)}
		if response['logged']:
			response['user'] = self.current_user
		self.write(response)
