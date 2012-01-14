import models

class UserAPI(object):
	def board_list(self, *args, **kwargs):
		return [b.public_info() for b in models.Board.objects]
