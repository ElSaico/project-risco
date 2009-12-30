from game import Game
from player import Player
from territory import Territory
from map import Map
from constants import validColors

b = Territory()
b.reinforce(8)
c = Territory()
c.reinforce(6)
while b.armySize > 3 and c.armySize > 3:
	b.attack(c, 3)
	print "b:", b.armySize, "c:", c.armySize

d = Map(validColors)
