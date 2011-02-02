import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from gameSprite import GameSprite

WHITE = (255, 255, 255)

class Label(GameSprite):
	img = None
	simg = None
	font_size = 16
	font = None
	maxLen = 20
	smaxLen = 4
	def __init__(self, screen, position, type=None):
		self.text = ""
		if not Label.font:
			Label.font = pygame.font.Font(None, Label.font_size)
		
		if type == "small":
			if not Label.simg:
				Label.simg = pygame.image.load("images/smalltext-area.png").convert_alpha()
			GameSprite.__init__(self, None, screen, Label.simg, position, False)
		else:
			if not Label.img:
				Label.img = pygame.image.load("images/text-area.png").convert_alpha()
			GameSprite.__init__(self, None, screen, Label.img, position, False)
		
		self.type = type
		
	def blitMe(self):
		self.screen.blit(self.image, self.pos)
		t = Label.font.render(self.text, True, WHITE)
		# heuristic method to prevent text larger than space avaible in label
		if t.get_width() / self.image.get_width() > 0.7:
			scale_constant = 1.7 - (t.get_width() / self.image.get_width())
			t = Label.font.render(self.text[:int(scale_constant * len(self.text))], True, WHITE)
		self.screen.blit(t, (self.pos[0] + 18, self.pos[1] + 5))
		pygame.display.update()
		
	def setText(self, text):
		if self.type == "small":
			self.text = text[:Label.smaxLen]
		else:
			self.text = text[:Label.maxLen]
		self.blitMe()
		
	def clear(self):
		self.setText("")
