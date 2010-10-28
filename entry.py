import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from gameSprite import GameSprite
import time
import string

WHITE = (255, 255, 255)

class Entry(GameSprite):
	img = None
	font_size = 16
	font = None
	maxLen = 15
	timerFreq = 1.0
	def __init__(self, screen, position):
		self.selected = False
		self.text = ""
		self.timer = time.time()
		pygame.init()
		if not Entry.font:
			Entry.font = pygame.font.Font(None, Entry.font_size)
		
		if not Entry.img:
			Entry.img = pygame.image.load("images/text-area.png").convert_alpha()
			
		GameSprite.__init__(self, None, screen, Entry.img, position, False)
		
	def blitMe(self):
		self.screen.blit(self.image, self.pos)
		blit_text = self.text
		if self.selected and self.getTime() < Entry.timerFreq / 2:
			blit_text += "_"
		self.updateTimer()
		t = Entry.font.render(blit_text, True, WHITE)
		self.screen.blit(t, (self.pos[0] + 18, self.pos[1] + 5))
		pygame.display.update()
		
	def mouseEvent(self, pos, clicked=True):
		if clicked:
			self.selected = self.pointIsInside(pos)
			self.blitMe()
		
	def keyPressed(self, key, caps=False):
		if self.selected and 0 < key < 256:
			if key == K_BACKSPACE:
				self.text = self.text[:len(self.text)-1]
			elif len(self.text) < Entry.maxLen:
				c = chr(key)
				if caps: c = string.upper(c)
				self.text += c
			self.blitMe()
			
	def getTime(self):
		return time.time() - self.timer
			
	def updateTimer(self):
		if self.getTime() > Entry.timerFreq:
			self.timer = time.time()
