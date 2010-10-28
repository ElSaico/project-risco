import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from gameSprite import GameSprite

class Button(GameSprite):
	img = None
	img_hover = None
	cimg = None
	cimg_hover = None
	font_size = 16
	font = None
	def __init__(self, name, screen, position, type=None):
		self.hover = False
		self.blocked = False
		if Button.font == None:
			Button.font = pygame.font.Font(None, Button.font_size)
		
		if type == "circular":
			if Button.cimg == None:
				Button.cimg = pygame.image.load("images/circularbutton.png").convert_alpha()
			if Button.cimg_hover == None:
				Button.cimg_hover = pygame.image.load("images/circularbutton_hover.png").convert_alpha()
			GameSprite.__init__(self, name, screen, Button.cimg, position, False)
		else:
			if Button.img == None:
				Button.img = pygame.image.load("images/button.png").convert_alpha()
			if Button.img_hover == None:
				Button.img_hover = pygame.image.load("images/button_hover.png").convert_alpha()
			GameSprite.__init__(self, name, screen, Button.img, position, False)
		
		self.type = type
	
	def blitMe(self):
		self.screen.blit(self.image, self.pos)
		if self.blocked:
			fontColor = (128, 128, 128)
		else:
			fontColor = (0, 0, 0)
		t = Button.font.render(self.name, True, fontColor)
		self.screen.blit(t, (self.pos[0] + (self.image.get_width() - t.get_width())/2, self.pos[1] + (self.image.get_height() - t.get_height())/2))
		
	def mouseEvent(self, pos):
		if self.pointIsInside(pos) and not self.blocked:
			self.swapState(True)
			return self.name
		self.swapState(False)
		return None	
		
	def swapState(self, mouseIsInside):
		updated = False
		if mouseIsInside and not self.hover:
			if self.type == "circular":
				self.image = Button.cimg_hover
			else:
				self.image = Button.img_hover
			updated = True
		elif not mouseIsInside and self.hover:
			if self.type == "circular":
				self.image = Button.cimg
			else:
				self.image = Button.img
			updated = True
		
		if updated:
			self.blitMe()
			self.hover = not self.hover
	
	def block(self):
		self.blocked = True
		self.blitMe()
		pygame.display.update()
	
	def unblock(self):
		self.blocked = False
		self.blitMe()
		pygame.display.update()
