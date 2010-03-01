import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from sys import exit
from game import Game
from player import Player
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
debug = True

class Interface:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
		self.screen.fill(BG_COLOR)
		pygame.display.set_caption('pyWar Online')
		self.font = pygame.font.Font("arial.ttf", FONT_SIZE)
		self.sprite = {}
		self.panel = {}
		self.source = None
		self.destination = None
		self.attacking = False
		self.relocating = False
	
	def clearArea(self, position, size):
		pygame.draw.rect(self.screen, BG_COLOR, Rect(position, size))
	
	def writeText(self, text, color, position):
		# params: string, true/false (anti-alias), cor
		t = self.font.render(text, True, color)
		self.screen.blit(t, position)
		pygame.display.update()
		
	def initializeLoadingBar(self, x):
		# vertical
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0]-LBAR_BORDER_SIZE, LBAR_POSITION[1]-LBAR_BORDER_SIZE), \
													(LBAR_BORDER_SIZE, FONT_SIZE + 2*LBAR_BORDER_SIZE)))
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0]+x*BAR_WIDTH, LBAR_POSITION[1]-LBAR_BORDER_SIZE), \
													(LBAR_BORDER_SIZE, FONT_SIZE + 2*LBAR_BORDER_SIZE)))
		
		# horizontal
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0]-LBAR_BORDER_SIZE, LBAR_POSITION[1]-LBAR_BORDER_SIZE), \
													(x*BAR_WIDTH + 2*LBAR_BORDER_SIZE, LBAR_BORDER_SIZE)))
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0]-LBAR_BORDER_SIZE, LBAR_POSITION[1]+FONT_SIZE), \
													(x*BAR_WIDTH + 2*LBAR_BORDER_SIZE, LBAR_BORDER_SIZE)))
		
		return 0
	
	def updateLoadingBar(self, loadingBarCounter):
		pygame.draw.rect(self.screen, WHITE, Rect((LBAR_POSITION[0] + loadingBarCounter*BAR_WIDTH, LBAR_POSITION[1]), (BAR_WIDTH, FONT_SIZE)))
		return loadingBarCounter + 1

	def loadImages(self, countries):
		self.writeText("Carregando Imagens...", WHITE, (WIDTH/6, 100))
		loadingBarCounter = self.initializeLoadingBar(len(countries)-1)
		for c in countries:
			filename = "images/{0}.png".format(c)
			self.sprite[c] = GameSprite(c, self.screen, pygame.image.load(filename).convert_alpha(), BOARD_POSITION)
			
			self.clearArea((WIDTH/3, 450), (225, FONT_SIZE+5))
			self.writeText(c, WHITE, (WIDTH/3, 450))
			loadingBarCounter = self.updateLoadingBar(loadingBarCounter)
		
		self.panel["Top"] = GameSprite(None, self.screen, pygame.image.load("images/panel-top.png").convert_alpha(), (0, 565))
		self.panel["BG"] = GameSprite(None, self.screen, pygame.image.load("images/panel.png").convert_alpha(), (0, 595))
		self.panel["Dice"] = GameSprite(None, self.screen, pygame.image.load("images/panel-dice.png").convert_alpha(), (756, 565))
		text_area = pygame.image.load("images/text-area.png").convert_alpha()
		self.textFrom = GameSprite(None, self.screen, text_area, (70, 615))
		self.textTo = GameSprite(None, self.screen, text_area, (70, 645))
		self.textCounter = GameSprite(None, self.screen, pygame.image.load("images/smalltext-area.png").convert_alpha(), (431, 617))
		self.background = GameSprite(None, self.screen, pygame.image.load("images/Fundo.png").convert_alpha(), BOARD_POSITION)
		self.foreground = GameSprite(None, self.screen, pygame.image.load("images/Topo.png").convert_alpha(), BOARD_POSITION)
		
		self.atkButton = Button("Atacar", self.screen, (600, 615))
		self.relocateButton = Button("Movimentar", self.screen, (600, 655))
		self.cancelButton = Button("Cancelar", self.screen, (600, 695))
		self.minusButton = Button("-", self.screen, (400, 617), "circular")
		self.plusButton = Button("+", self.screen, (500, 617), "circular")
		self.nextStepButton = Button("Proxima Etapa", self.screen, (400, 655))
		
		self.redDice = []
		self.yellowDice = []
		for i in range(6):
			self.redDice.append(GameSprite(None, self.screen, pygame.image.load("images/red{0}.png".format(i+1)).convert_alpha(), (0, 0)))
			self.yellowDice.append(GameSprite(None, self.screen, pygame.image.load("images/yellow{0}.png".format(i+1)).convert_alpha(), (0, 0)))
			

	def draw_screen(self):
		self.background.blitMe()
		for country in self.sprite.values():
			country.blitMe()
		self.foreground.blitMe()
		self.drawPanel()
		pygame.display.update()
		
	def drawPanel(self):
		for element in self.panel.values():
			element.blitMe()
		self.textTo.blitMe()
		self.textFrom.blitMe()
		self.textCounter.blitMe()
		self.atkButton.blitMe()
		self.relocateButton.blitMe()
		self.cancelButton.blitMe()
		self.minusButton.blitMe()
		self.plusButton.blitMe()
		self.nextStepButton.blitMe()
		
		pygame.display.update()
		
	def cleanDice(self):
		pass
		
	def printDice(self, diceAtk, diceDef):
		for i, v in enumerate(diceAtk):
			self.redDice[v-1].pos = (780 + i*70, 600)
			self.redDice[v-1].blitMe()
		for i, v in enumerate(diceDef):
			self.yellowDice[v-1].pos = (780 + i*70, 675)
			self.yellowDice[v-1].blitMe()
		
	def eventHandler(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				button = None
				button = button or self.atkButton.mouseEvent(pygame.mouse.get_pos()) ###
				button = button or self.relocateButton.mouseEvent(pygame.mouse.get_pos()) ###
				button = button or self.cancelButton.mouseEvent(pygame.mouse.get_pos()) ###
				button = button or self.minusButton.mouseEvent(pygame.mouse.get_pos()) ###
				button = button or self.plusButton.mouseEvent(pygame.mouse.get_pos()) ###
				button = button or self.nextStepButton.mouseEvent(pygame.mouse.get_pos()) ###
				
					
				if self.game.step == "Trade":
					self.atkButton.block()
					self.relocateButton.block()
					if button == "Proxima Etapa":
						self.minusButton.block()
						self.plusButton.block()
						self.game.nextStep()
				elif self.game.step == "Reinforce":
					if button == "Proxima Etapa":
						for t, n in self.toReinforce.items():
							if self.game.ownCountry(self.game.turn, t):
								self.game.reinforce(t, n)
							self.toReinforce[t] = 0
						self.source = None
						self.destination = None
						self.textTo.blitMe()
						self.plusButton.block()
						self.minusButton.block()
						self.game.nextStep()
						
					if debug:
						print self.game.turn, self.toReinforce.values()
						
					for country in self.sprite.values():
						territory = country.mouseEvent(pygame.mouse.get_pos())
						if territory:
							self.destination = territory
							break
						
					if self.destination and \
					   self.game.ownCountry(self.game.turn, self.destination):
						self.textTo.blitMe()
						self.writeText(self.destination, WHITE, (90, 650))
						if button == "+" and not self.plusButton.blocked:
							self.toReinforce[self.destination] += 1
						elif button == "-" and not self.minusButton.blocked:
							self.toReinforce[self.destination] -= 1
						self.textCounter.blitMe()
						self.writeText(str(self.toReinforce[self.destination]), WHITE, (450, 621))
					else:
						self.plusButton.block()
						self.minusButton.block()
						self.textTo.blitMe()
						self.textCounter.blitMe()
					
					if sum(self.toReinforce.values()) >= self.game.reinforcements:
						self.plusButton.block()
					elif self.plusButton.blocked:
						self.plusButton.unblock()
					
					if sum(self.toReinforce.values()) <= 0 or \
					      (self.destination and \
					       self.toReinforce[self.destination] <= 0):
						self.minusButton.block()
					elif self.minusButton.blocked:
						self.minusButton.unblock()
				elif self.game.step == "Attack" or self.game.step == "Relocate":
					if button == "Proxima Etapa":
						if self.game.step == "Attack":
							self.atkButton.block()
						elif self.game.step == "Relocate":
							self.relocateButton.block()
						self.source = None
						self.destination = None
						self.textFrom.blitMe()
						self.textTo.blitMe()
						self.plusButton.block()
						self.minusButton.block()
						self.game.nextStep()
						
					for country in self.sprite.values():
						territory = country.mouseEvent(pygame.mouse.get_pos())
						if territory:
							if not self.source:
								self.source = territory
								break
							elif self.source and self.game.ownCountry(self.game.turn, territory):
								self.source = territory
								self.destination = None
								break
							elif self.game.worldmap.neighbors(self.source, territory):
								self.counter = 0
								self.textCounter.blitMe()
								self.writeText(str(self.counter), WHITE, (450, 621))
								self.plusButton.unblock()
								self.destination = territory
								break
								
					if button == "Cancelar":
						self.source = None
						self.destination = None
						self.textFrom.blitMe()
						self.textTo.blitMe()
						self.textCounter.blitMe()
								
					if self.source and \
						self.game.ownCountry(self.game.turn, self.source):
							self.textFrom.blitMe()
							self.writeText(self.source, WHITE, (90, 620))
					else:
						self.source = None
						self.textFrom.blitMe()
					
					if self.destination and \
						not self.game.ownCountry(self.game.turn, self.destination):
							self.textTo.blitMe()
							self.writeText(self.destination, WHITE, (90, 650))
							
							if button == "+":
								self.counter += 1
								if self.minusButton.blocked:
									self.minusButton.unblock()
								if self.game.step == "Relocate" and self.relocateButton.blocked:
									self.relocateButton.unblock()
								self.textCounter.blitMe()
								self.writeText(str(self.counter), WHITE, (450, 621))
							elif button == "-":
								self.counter -= 1
								if self.plusButton.blocked:
									self.plusButton.unblock()
								self.textCounter.blitMe()
								self.writeText(str(self.counter), WHITE, (450, 621))
							
							if self.game.step == "Attack":
								if self.counter >= 3:
									self.counter = 3
									self.plusButton.block()
								if self.counter > 0 and self.atkButton.blocked:
									self.atkButton.unblock()
							elif self.game.step == "Relocate":
								if self.counter > 0 and self.relocateButton.blocked:
									self.relocateButton.unblock()
									
							if self.counter >= self.game.worldmap.country(self.source).armySize:
								self.counter = self.game.worldmap.country(self.source).armySize - 1
								self.plusButton.block()
							
							if self.counter <= 0:
								self.counter = 0
								self.minusButton.block()
								if self.game.step == "Attack" and not self.atkButton.blocked:
									self.atkButton.block()
								if self.game.step == "Relocate" and not self.relocateButton.blocked:
									self.relocateButton.block()
					else:
						self.destination = None
						self.textTo.blitMe()
						
					if self.game.step == "Attack":
						if button == "Atacar":
							atkReturn = self.game.attack(self.source, self.destination, self.counter)
							self.printDice(atkReturn[1], atkReturn[2])
							self.minusButton.block()
							self.plusButton.unblock()
							self.counter = 0
							self.textCounter.blitMe()
							self.writeText(str(self.counter), WHITE, (450, 621))
					elif self.game.step == "Relocate":
						if button == "Movimentar":
							self.game.relocate(self.source, self.destination, self.counter)
							self.relocateButton.block()
							self.atkButton.block()
							self.textCounter.blitMe()
		
		self.atkButton.mouseEvent(pygame.mouse.get_pos()) ###
		self.relocateButton.mouseEvent(pygame.mouse.get_pos()) ###
		self.cancelButton.mouseEvent(pygame.mouse.get_pos()) ###
		self.minusButton.mouseEvent(pygame.mouse.get_pos()) ###
		self.plusButton.mouseEvent(pygame.mouse.get_pos()) ###
		self.nextStepButton.mouseEvent(pygame.mouse.get_pos()) ###
		
		for country in self.sprite.values():
			territory = country.mouseEvent(pygame.mouse.get_pos())
			if territory != None:
				if territory != self.lastHover:
					# just testing, not done yet...
					self.panel["Top"].blitMe()
					self.writeText("{0} ({1.armySize}) - {1.owner}".format(territory, self.game.worldmap.country(territory)), WHITE, (10, 572))
					self.lastHover = territory
				break

	def mainLoop(self):
		self.game = Game("map.json", False)
		self.game.addPlayer(Player("White"))
		self.game.addPlayer(Player("Black"))
		self.game.start()
		self.lastHover = None #tirar depois...
		self.counter = 0
		self.screen.fill(BG_COLOR)
		self.loadImages(self.game.worldmap.countries())
		self.screen.fill(BG_COLOR)
		self.font = pygame.font.Font("arial.ttf", 16)
		self.draw_screen()
		self.toReinforce = dict((x, 0) for x in self.game.worldmap.countries())
		while True:
			self.eventHandler()
			
	def menu(self):
		bg = GameSprite(None, self.screen, pygame.image.load("images/menu_bg.png").convert_alpha(), (0, 0))
		logo_img = pygame.image.load("images/logo.png").convert_alpha()
		logo = GameSprite(None, self.screen, logo_img, ((WIDTH - logo_img.get_width())/2, (HEIGHT - logo_img.get_height())/4))
		newgame = Button("Novo Jogo", self.screen, (450, 590))
		
		bg.blitMe()
		logo.blitMe()
		newgame.blitMe()
		pygame.display.update()
		
		while True:
			button = newgame.mouseEvent(pygame.mouse.get_pos())
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					exit()
				elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
					if button == "Novo Jogo":
						self.mainLoop()
			

a = Interface()
a.menu()
#a.mainLoop()
