from game import Game
from player import Player
from territory import Territory

a = Player("White")
print a

b = Territory("White")
b.reinforce(8)
c = Territory("Blue")
c.reinforce(6)
while b.armySize > 3 and c.armySize > 3:
	b.attack(c, 3)
	print "b:", b.armySize, "c:", c.armySize
