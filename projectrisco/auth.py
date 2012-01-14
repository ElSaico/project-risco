from tornado.web import asynchronous, HTTPError, RequestHandler
from tornado.auth import GoogleMixin
from tornado.escape import json_encode

import models

class GoogleHandler(RequestHandler, GoogleMixin):
	@asynchronous
	def get(self):
		if self.get_argument("openid.mode", None):
			self.get_authenticated_user(self.async_callback(self._on_auth))
			return
		self.authenticate_redirect()
	
	def _on_auth(self, user):
		if not user:
			raise HTTPError(500, "Google auth failed")
		user_obj, created = models.GoogleUser.objects.get_or_create(email=user['email'])
		for field, value in user.items():
			setattr(user_obj, field, value)
		user_obj.save()
		user['id'] = str(user_obj._id)
		user['identity'] = self.get_argument('openid.identity', None)
		self.set_secure_cookie('auth', json_encode(user))
		self.redirect('/')
