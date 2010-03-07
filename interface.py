import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from sys import exit
from game import Game
from player import Player
from gameSprite import GameSprite
from button import Button
from entry import Entry
from label import Label
from socket import *
from communication.communication_pb2 import ClientToServer, ServerToClient

import struct

BLACK, WHITE = (0, 0, 0), (255, 255, 255)
BG_COLOR = BLACK
WIDTH, HEIGHT = 1024, 768
FONT_SIZE = 32
BOARD_POSITION = (0, 0)
BAR_WIDTH = 10
LBAR_POSITION = (WIDTH/3, 500)
LBAR_BORDER_SIZE = 2
SOCKET, IP, COLOR = 0, 1, 2
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
		self.font = pygame.font.Font("arial.ttf", FONT_SIZE)
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
		self.textFrom = Label(self.screen, (70, 615))
		self.textTo = Label(self.screen, (70, 645))
		self.textTurn = Label(self.screen, (70, 695))
		self.textCounter = Label(self.screen, (431, 617), "small")
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
		self.textTurn.blitMe()
		self.atkButton.blitMe()
		self.relocateButton.blitMe()
		self.cancelButton.blitMe()
		self.minusButton.blitMe()
		self.plusButton.blitMe()
		self.nextStepButton.blitMe()
		
		pygame.display.update()
		
	def cleanDice(self):
		self.panel["Dice"].blitMe()
		
	def printDice(self, diceAtk, diceDef):
		self.cleanDice()
		for i, v in enumerate(diceAtk):
			self.redDice[v-1].pos = (780 + i*70, 600)
			self.redDice[v-1].blitMe()
		for i, v in enumerate(diceDef):
			self.yellowDice[v-1].pos = (780 + i*70, 675)
			self.yellowDice[v-1].blitMe()
			
	def trade(self, button):
		self.atkButton.block()
		self.relocateButton.block()
		if button == "Proxima Etapa":
			self.minusButton.block()
			self.plusButton.block()
			self.game.nextStep()
			self.textTurn.setText("{0} - {1}".format(self.game.turn, self.game.step))
		
	def reinforce(self, button):
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
			self.textTurn.setText("{0} - {1}".format(self.game.turn, self.game.step))
			
		if debug:
			print self.game.turn, self.toReinforce.values()
			
		for country in self.sprite.values():
			territory = country.mouseEvent(pygame.mouse.get_pos())
			if territory:
				self.destination = territory
				break
			
		if self.destination and \
		   self.game.ownCountry(self.game.turn, self.destination):
			self.textTo.setText(self.destination)
			if button == "+" and not self.plusButton.blocked:
				self.toReinforce[self.destination] += 1
			elif button == "-" and not self.minusButton.blocked:
				self.toReinforce[self.destination] -= 1
			self.textCounter.setText(str(self.toReinforce[self.destination]))
		else:
			self.plusButton.block()
			self.minusButton.block()
			self.textTo.clear()
			self.textCounter.clear()
		
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
		
	def attack_or_relocate(self, button):
		if button == "Proxima Etapa":
			if self.game.step == "Attack":
				self.cleanDice()
				self.atkButton.block()
			elif self.game.step == "Relocate":
				self.relocateButton.block()
			self.source = None
			self.destination = None
			self.textFrom.clear()
			self.textTo.clear()
			self.plusButton.block()
			self.minusButton.block()
			self.game.nextStep()
			self.textTurn.setText("{0} - {1}".format(self.game.turn, self.game.step))
			
		for country in self.sprite.values():
			territory = country.mouseEvent(pygame.mouse.get_pos())
			if territory:
				if not self.source:
					self.source = territory
					break
				elif self.source and self.game.ownCountry(self.game.turn, territory) and self.game.step == "Attack":
					self.source = territory
					self.destination = None
					break
				elif self.game.worldmap.neighbors(self.source, territory):
					self.counter = 0
					self.textCounter.setText(str(self.counter))
					self.plusButton.unblock()
					self.destination = territory
					break
					
		if button == "Cancelar":
			self.source = None
			self.destination = None
			self.textFrom.clear()
			self.textTo.clear()
			self.textCounter.clear()
					
		if self.source and \
			self.game.ownCountry(self.game.turn, self.source):
				self.textFrom.setText(self.source)
		else:
			self.source = None
			self.textFrom.clear()
		
		if self.destination and \
			((self.game.step == "Attack" and not self.game.ownCountry(self.game.turn, self.destination)) \
			or (self.game.step == "Relocate" and self.game.ownCountry(self.game.turn, self.destination))):
				self.textTo.setText(self.destination)
				
				if button == "+":
					self.counter += 1
					if self.minusButton.blocked:
						self.minusButton.unblock()
					if self.game.step == "Relocate" and self.relocateButton.blocked:
						self.relocateButton.unblock()
					
				elif button == "-":
					self.counter -= 1
					if self.plusButton.blocked:
						self.plusButton.unblock()
				
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
						
				self.textCounter.setText(str(self.counter))
		else:
			self.destination = None
			self.textTo.clear()
			
		if self.game.step == "Attack":
			if button == "Atacar":
				atkReturn = self.game.attack(self.source, self.destination, self.counter)
				self.printDice(atkReturn[1], atkReturn[2])
				if atkReturn[0]:
					self.destination = None
					self.textTo.clear()
				self.atkButton.block()
				self.minusButton.block()
				self.plusButton.unblock()
				self.counter = 0
				self.textCounter.setText(str(self.counter))
		elif self.game.step == "Relocate":
			if button == "Movimentar":
				self.game.relocate(self.source, self.destination, self.counter)
				self.relocateButton.block()
				self.atkButton.block()
				self.textCounter.clear()
		
	def eventHandler(self):
		button = None
		button = button or self.atkButton.mouseEvent(pygame.mouse.get_pos()) ###
		button = button or self.relocateButton.mouseEvent(pygame.mouse.get_pos()) ###
		button = button or self.cancelButton.mouseEvent(pygame.mouse.get_pos()) ###
		button = button or self.minusButton.mouseEvent(pygame.mouse.get_pos()) ###
		button = button or self.plusButton.mouseEvent(pygame.mouse.get_pos()) ###
		button = button or self.nextStepButton.mouseEvent(pygame.mouse.get_pos()) ###
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				exit()
			elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:	
				if self.game.step == "Trade":
					self.trade(button)
				elif self.game.step == "Reinforce":
					self.reinforce(button)
				elif self.game.step == "Attack" or self.game.step == "Relocate":
					self.attack_or_relocate(button)
		
		for country in self.sprite.values():
			territory = country.mouseEvent(pygame.mouse.get_pos())
			if territory != None:
				# just testing, not done yet...
				self.panel["Top"].blitMe()
				self.writeText("{0} ({1.armySize}) - {1.owner}".format(territory, self.game.worldmap.country(territory)), WHITE, (10, 572))
				break

	def mainLoop(self):
		if self.type == "Server":
			self.game = Game("map.json", False)
			for c in self.clients:
				self.game.addPlayer(Player(c[COLOR]))
			self.game.start()
			stc = ServerToClient()
			assert len(stc.territory_info) == 0
			for name, territory in self.game.worldmap._countries.items():
				t = stc.territory_info.add()
				t.name = name
				t.owner = territory.owner
				t.size = territory.armySize
			assert len(stc.territory_info) == len(self.game.worldmap._countries)
			assert len(stc.edge) == 0
			for link1, link2 in self.game.worldmap._borders:
				e = stc.edge.add()
				e.node1 = link1
				e.node2 = link2
			assert len(stc.edge) == 0
			stcS = stc.SerializeToString()
			for c in self.clients:
				c[SOCKET].send(stcS)
		elif self.type == "Client":
			pass
		self.counter = 0
		self.screen.fill(BG_COLOR)
		self.loadImages(self.game.worldmap.countries())
		self.screen.fill(BG_COLOR)
		self.font = pygame.font.Font("arial.ttf", 16)
		self.draw_screen()
		self.textTurn.setText("{0} - {1}".format(self.game.turn, self.game.step))
		self.toReinforce = dict((x, 0) for x in self.game.worldmap.countries())
		while True:
			self.receiveInfo()
			self.eventHandler()
			
	def receiveInfo(self):
		pass
			
	def enterGame(self):
		colorEntry = Entry(self.screen, (425, 360))
		ipEntry = Entry(self.screen, (425, 400))
		ok = Button("OK", self.screen, (450, 490))
		self.font = pygame.font.Font("arial.ttf", 20)
		
		self.bg.blitMe()
		self.logo.blitMe()
		ok.block()
		ipEntry.blitMe()
		colorEntry.blitMe()
		self.writeText("Color:", WHITE, (370, 363))
		self.writeText("IP:", WHITE, (390, 403))
		pygame.key.set_repeat(150, 75)
		
		while True:
			button = ok.mouseEvent(pygame.mouse.get_pos())
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					exit()
				elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
					ipEntry.mouseEvent(pygame.mouse.get_pos())
					colorEntry.mouseEvent(pygame.mouse.get_pos())
					if button == "OK":
						self.client = socket(AF_INET, SOCK_STREAM)
						self.client.connect((ipEntry.text, 2300))
						cts = ClientToServer()
						assert not cts.HasField("player_info")
						cts.player_info.color = colorEntry.text
						assert cts.HasField("player_info")
						self.client.send(cts.SerializeToString())
						self.mainLoop()
				elif event.type == KEYDOWN:
					ipEntry.keyPressed(event.key, pygame.key.get_mods() & (KMOD_CAPS | KMOD_SHIFT))
					colorEntry.keyPressed(event.key, pygame.key.get_mods() & (KMOD_CAPS | KMOD_SHIFT))
					if ipEntry.text != "" and colorEntry.text != "" and ok.blocked:
						ok.unblock()
					elif (ipEntry.text == "" or colorEntry.text == "") and not ok.blocked:
						ok.block()
				
			if ipEntry.selected:
				ipEntry.blitMe()
			if colorEntry.selected:
				colorEntry.blitMe()
	
	def createGame(self):
		self.server = socket(AF_INET, SOCK_STREAM)
		self.server.bind(('', 2300))
		self.server.listen(2)
		self.server.settimeout(0.0)
		self.clients = []
		self.clients.append(("Juca", "127.0.0.1", "White"))
		self.mainLoop()
		ok = Button("OK", self.screen, (450, 490))
		
		self.bg.blitMe()
		self.logo.blitMe()
		ok.block()
		BUFSIZE = 4096
		while True:
			#print "waiting for connection..."
			try:
				clientsock, addr = self.server.accept()
				if clientsock:
					clientsock.settimeout(0.5)
					data = clientsock.recv(BUFSIZE)
					while not data:
						data = clientsock.recv(BUFSIZE)
					
					cts = ClientToServer()
					cts.ParseFromString(data)
					if cts.HasField("player_info"):
						playing = False
						for c in self.clients:
							if c[IP] == addr[0] or c[COLOR] == cts.player_info.color:
								playing = True
								print "Refused connection from:", cts.player_info.color, addr[0]
						# also need to check if the received color is different from self color
						# and if the received color is valid
						if not playing:
							print cts.player_info.color, "connected from", addr[0]
							self.clients.append((clientsock, addr[0], cts.player_info.color))
							self.clearArea((400, 720), (200, 50))
							self.writeText("{0} - {1}".format(cts.player_info.color, addr[0]), WHITE, (400, 720))
			except:
				pass
				
			if len(self.clients) > 0 and ok.blocked: # temporary, the number of clients should be configurable
				ok.unblock()
			
			button = ok.mouseEvent(pygame.mouse.get_pos())
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					exit()
				elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
					if button == "OK":
						self.mainLoop()
				
		self.mainLoop()
			
	def menu(self):
		self.bg = GameSprite(None, self.screen, pygame.image.load("images/menu_bg.png").convert_alpha(), (0, 0))
		logo_img = pygame.image.load("images/logo.png").convert_alpha()
		self.logo = GameSprite(None, self.screen, logo_img, ((WIDTH - logo_img.get_width())/2, (HEIGHT - logo_img.get_height())/4))
		
		newgame = Button("Novo Jogo", self.screen, (450, 590))
		entergame = Button("Entrar em Jogo", self.screen, (450, 635))
		
		self.bg.blitMe()
		self.logo.blitMe()
		newgame.blitMe()
		entergame.blitMe()
		pygame.display.update()
		
		while True:
			button = newgame.mouseEvent(pygame.mouse.get_pos())
			button = button or entergame.mouseEvent(pygame.mouse.get_pos())
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					exit()
				elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
					if button == "Novo Jogo":
						self.type = "Server"
						self.createGame()
					elif button == "Entrar em Jogo":
						self.type = "Client"
						self.enterGame()
						
						
			

a = Interface()
a.menu()
#a.mainLoop()
