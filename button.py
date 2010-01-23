import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from gameSprite import GameSprite

class Button(GameSprite):
	img = None
	img_hover = None
	font_size = 16
	font = None
	def __init__(self, name, screen, position):
		self.hover = False
		pygame.init()
		if Button.img == None:
			Button.img = pygame.image.load("images/button.png").convert_alpha()
		if Button.img_hover == None:
			Button.img_hover = pygame.image.load("images/button_hover.png").convert_alpha()
		if Button.font == None:
			Button.font = pygame.font.Font("arial.ttf", Button.font_size)
		self.blocked = False
		GameSprite.__init__(self, name, screen, Button.img, position, False)
	
	def blitMe(self):
		self.screen.blit(self.image, self.pos)
		if self.blocked:
			fontColor = (128, 128, 128)
		else:
			fontColor = (0, 0, 0)
		t = Button.font.render(self.name, True, fontColor)
		self.screen.blit(t, (self.pos[0] + (self.image.get_width() - t.get_width())/2, self.pos[1] + (self.image.get_height() - t.get_height())/2))
		pygame.display.update()
		
	def mouseEvent(self, pos):
		if self.pointIsInside(pos) and not self.blocked:
			self.swapState(True)
			return self.name
		self.swapState(False)
		return None	
		
	def swapState(self, mouseIsInside):
		updated = False
		if mouseIsInside and not self.hover:
			self.image = Button.img_hover
			updated = True
		elif not mouseIsInside and self.hover:
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