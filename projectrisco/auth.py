from tornado.web import asynchronous, HTTPError
from tornado.auth import GoogleMixin
from tornado.escape import json_encode

from common import RiscoHandler

class GoogleHandler(RiscoHandler, GoogleMixin):
	@asynchronous
	def get(self):
		if self.get_argument("openid.mode", None):
			self.get_authenticated_user(self.async_callback(self._on_auth))
			return
		self.authenticate_redirect()
	
	def _on_auth(self, user):
		if not user:
			raise HTTPError(500, "Google auth failed")
		self.database.users.update({'email': user['email']}, user, upsert=True)
		user_obj = self.database.users.find_one({'email': user['email']})
		user['id'] = str(user_obj['_id'])
		user['identity'] = self.get_argument('openid.identity', None)
		self.set_secure_cookie('auth', json_encode(user))
		self.redirect('/')
