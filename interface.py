import pygame
from pygame.locals import *
from pygame.sprite import Sprite
from constants import countries

def adjust_image(image, screen):
	img_w = image.get_width()
	img_h = image.get_height()
	scr_aspect = screen.get_width() / screen.get_height()
	img_aspect = img_w * 1.0 / img_h
	if img_aspect > scr_aspect:
		img_w = screen.get_width()
		img_h = (int)(img_w / img_aspect)
	else:
		img_h = screen.get_height()
		img_w = (int)(img_h * img_aspect)
	return pygame.transform.smoothscale(image, (img_w,img_h))

class TerritorySprite(Sprite):
	def __init__(self, name, screen, img_filename, position):
		Sprite.__init__(self)
		self.name = name
		self.screen = screen
		self.pos = position
		self.image = pygame.image.load(img_filename).convert_alpha()
		# resize to fit screen
		self.image = adjust_image(self.image, self.screen)
	
	def blitme(self):
		self.screen.blit(self.image, self.pos)

	def mouse_click_event(self, pos):
		if self._point_is_inside(pos):
			print "Clicked inside " + self.name + "!"
	
	def mouse_focusing_event(self, pos):
		if self._point_is_inside(pos):
			return self.name
		return None
			
	def _point_is_inside(self, point):
		try:
			pix = self.image.get_at(point)
			return pix[3] > 0
		except IndexError:
			return False


pygame.init()
BG_COLOR = (0, 0, 0)
width = 1024
height = 768
screen = pygame.display.set_mode((width,height),0,32)
pygame.display.set_caption('pyWar Online')

screen.fill(BG_COLOR)

font_size = 32
fonte = pygame.font.Font("arial.ttf", font_size)
# params: string, true/false (anti-alias), cor
texto = fonte.render("Carregando Imagens...", True, (255,255,255))
screen.blit(texto, (200,300))
pygame.display.update()
print "Charging Images..."
sprite = {}
counter = 0
for continent, lst in countries.items():
	for country in lst:
		filename = "images/" + country + ".png"
		img = pygame.image.load(filename).convert_alpha()
		#sprite[country] = TerritorySprite(country, screen, filename, (width/2 - img.get_width()/2, height/2 - img.get_height()/2))
		sprite[country] = TerritorySprite(country, screen, filename, (0, 0))
		texto = fonte.render(country, True, (255,255,255), (0, 0, 0))
		pygame.draw.rect(screen, (0, 0, 0), Rect((300, 400), (225, font_size)))
		bar_width = 10
		pygame.draw.rect(screen, (255, 255, 255), Rect((150 + counter*bar_width, 500), (bar_width, font_size)))
		counter += 1
		screen.blit(texto, (300,400))
		pygame.display.update()
print "Images Charged!"

fundo_file = "images/Fundo.png"
fundo = pygame.image.load(fundo_file).convert_alpha()
fundo = adjust_image(fundo, screen)
fundo_w = fundo.get_width()
fundo_h = fundo.get_height()

topo_file = "images/Topo.png"
topo = pygame.image.load(topo_file).convert_alpha()
topo = adjust_image(topo, screen)
topo_w = fundo.get_width()
topo_h = fundo.get_height()

def draw_screen(screen, territories, fundo, topo):
	screen.blit(fundo, (0, 0))
	for country in territories.keys():
		territories[country].blitme()
	screen.blit(topo, (0, 0))

draw_screen(screen, sprite, fundo, topo)
while True:
	input = False
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
		if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
			for country in sprite.keys():
				sprite[country].mouse_click_event(pygame.mouse.get_pos())
			# print "Left Mouse Button clicked!"
	
	for country in sprite.keys():
		a = sprite[country].mouse_focusing_event(pygame.mouse.get_pos())
		if a != None:
			print a

	pygame.display.update()
