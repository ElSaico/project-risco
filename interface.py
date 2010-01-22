import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from sys import exit
from globals import debug
from map import Map
from gameSprite import GameSprite
from button import Button

BLACK, WHITE = (0, 0, 0), (255, 255, 255)
BG_COLOR = BLACK
WIDTH, HEIGHT = 1024, 768
FONT_SIZE = 32
BOARD_POSITION = (0, 0)
BAR_WIDTH = 10
LBAR_POSITION = (WIDTH/3, 500)
LBAR_BORDER_SIZE = 2

class Interface:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
		self.screen.fill(BG_COLOR)
		pygame.display.set_caption('pyWar Online')
		self.font = pygame.font.Font("arial.ttf", FONT_SIZE)
		self.sprite = {}
		self.loadingBarCounter = 0
		self.background = None
		self.foreground = None
		self.panel = {}
		self.attackSrc = None
		self.attackDst = None
		self.atkButton = None
		self.cancelButton = None
	
	def clearArea(self, position, size):
		pygame.draw.rect(self.screen, BG_COLOR, Rect(position, size))
	
	def writeText(self, text, color, position):
		# params: string, true/false (anti-alias), cor
		t = self.font.render(text, True, color)
		self.screen.blit(t, position)
		pygame.display.update()
		
	def initializeLoadingBar(self, x):
		self.loadingBarCounter = 0
		
		# vertical
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0]-LBAR_BORDER_SIZE, LBAR_POSITION[1]-LBAR_BORDER_SIZE), (LBAR_BORDER_SIZE, FONT_SIZE + 2*LBAR_BORDER_SIZE)))
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0]+x*BAR_WIDTH, LBAR_POSITION[1]-LBAR_BORDER_SIZE), (LBAR_BORDER_SIZE, FONT_SIZE + 2*LBAR_BORDER_SIZE)))
		
		# horizontal
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0]-LBAR_BORDER_SIZE, LBAR_POSITION[1]-LBAR_BORDER_SIZE), (x*BAR_WIDTH + 2*LBAR_BORDER_SIZE, LBAR_BORDER_SIZE)))
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0]-LBAR_BORDER_SIZE, LBAR_POSITION[1]+FONT_SIZE), (x*BAR_WIDTH + 2*LBAR_BORDER_SIZE, LBAR_BORDER_SIZE)))
	
	def updateLoadingBar(self):
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0] + self.loadingBarCounter*BAR_WIDTH, LBAR_POSITION[1]), (BAR_WIDTH, FONT_SIZE)))
		self.loadingBarCounter += 1

	def loadImages(self, countries):
		self.writeText("Carregando Imagens...", WHITE, (WIDTH/6, 100))
		self.initializeLoadingBar(len(countries)-1)
		for c in countries:
			filename = "images/{0}.png".format(c)
			self.sprite[c] = GameSprite(c, self.screen, pygame.image.load(filename).convert_alpha(), BOARD_POSITION)
			
			self.clearArea((WIDTH/3, 450), (225, FONT_SIZE+5))
			self.writeText(c, WHITE, (WIDTH/3, 450))
			self.updateLoadingBar()
		
		self.panel["Top"] = GameSprite(None, self.screen, pygame.image.load("images/panel-top.png").convert_alpha(), (0, 565))
		self.panel["BG"] = GameSprite(None, self.screen, pygame.image.load("images/panel.png").convert_alpha(), (0, 595))
		self.panel["Dices"] = GameSprite(None, self.screen, pygame.image.load("images/panel-dices.png").convert_alpha(), (756, 565))
		text_area = pygame.image.load("images/text-area.png").convert_alpha()
		self.textFrom = GameSprite(None, self.screen, text_area, (70, 615))
		self.textTo = GameSprite(None, self.screen, text_area, (70, 645))
		self.background = GameSprite(None, self.screen, pygame.image.load("images/Fundo.png").convert_alpha(), BOARD_POSITION)
		self.foreground = GameSprite(None, self.screen, pygame.image.load("images/Topo.png").convert_alpha(), BOARD_POSITION)
		
		self.atkButton = Button("Atacar", self.screen, (600, 615))
		self.relocateButton = Button("Movimentar", self.screen, (600, 655))
		self.cancelButton = Button("Cancelar", self.screen, (600, 695))

	def draw_screen(self):
		self.background.blitMe()
		for country in self.sprite.values():
			country.blitMe()
		self.foreground.blitMe()
		for element in self.panel.values():
			element.blitMe()
		self.drawPanel()
		pygame.display.update()
		
	def drawPanel(self):
		for element in self.panel.values():
			element.blitMe()
		self.textTo.blitMe()
		self.textFrom.blitMe()
		self.atkButton.blitMe()
		self.relocateButton.blitMe()
		self.cancelButton.blitMe()
		pygame.display.update()
		
	def eventHandler(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				button = self.atkButton.mouseEvent(pygame.mouse.get_pos()) ###
				button = self.relocateButton.mouseEvent(pygame.mouse.get_pos()) ###
				button = self.cancelButton.mouseEvent(pygame.mouse.get_pos()) ###
				
				if button == "Cancelar":
					self.attackSrc = None
					self.attackDst = None
					self.textFrom.blitMe()
					self.textTo.blitMe()
					pygame.display.update()
				else:
					for country in self.sprite.values():
						territory = country.mouseEvent(pygame.mouse.get_pos())
						if territory != None:
							# just testing, not done yet...
							if self.attackSrc == None:
								self.attackSrc = territory
								self.textFrom.blitMe()
								self.writeText(territory, WHITE, (90, 620))
							else:
								self.attackDst = territory
								self.textTo.blitMe()
								self.writeText(territory, WHITE, (90, 650))
		
		self.atkButton.mouseEvent(pygame.mouse.get_pos()) ###
		self.relocateButton.mouseEvent(pygame.mouse.get_pos()) ###
		self.cancelButton.mouseEvent(pygame.mouse.get_pos()) ###
		
		for country in self.sprite.values():
			territory = country.mouseEvent(pygame.mouse.get_pos())
			if territory != None:
				if territory != self.lastHover:
					# just testing, not done yet...
					self.panel["Top"].blitMe()
					self.writeText(territory, WHITE, (10, 572))
					self.lastHover = territory
				break

	def mainLoop(self):
		m = Map(["White"])
		self.lastHover = None #tirar depois...
		self.loadImages(m.countries())
		self.screen.fill(BG_COLOR)
		self.font = pygame.font.Font("arial.ttf", 16)
		self.draw_screen()
		while True:
			self.eventHandler()

a = Interface()
a.mainLoop()
