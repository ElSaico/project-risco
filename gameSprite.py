import pygame
from pygame.locals import *
from pygame.sprite import Sprite

class GameSprite(Sprite):
	def __init__(self, name, screen, img, position, adjust=True):
		Sprite.__init__(self)
		self.name = name
		self.screen = screen
		self.pos = position
		self.image = img
		# resize to fit screen
		if self.image != None and adjust:
			self.adjustImage()
	
	def blitMe(self):
		self.screen.blit(self.image, self.pos)

	def mouseEvent(self, pos):
		if self.pointIsInside(pos):
			return self.name
		return None
			
	def pointIsInside(self, point):
		try:
			pix = self.image.get_at((point[0] - self.pos[0], point[1] - self.pos[1]))
			return pix[3] > 0
		except IndexError:
			return False
			
	def adjustImage(self):
		img_w = self.image.get_width()
		img_h = self.image.get_height()
		scr_aspect = self.screen.get_width() / self.screen.get_height()
		img_aspect = img_w * 1.0 / img_h
		if img_aspect > scr_aspect:
			img_w = self.screen.get_width()
			img_h = int(img_w / img_aspect)
		else:
			img_h = self.screen.get_height()
			img_w = int(img_h * img_aspect)
		self.image = pygame.transform.smoothscale(self.image, (img_w,img_h))
