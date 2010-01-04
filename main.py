# coding: utf-8
from game import Game
from player import Player
from territory import Territory
from map import Map
from constants import validColors

# b = Territory()
# b.setOwner("White")
# b.reinforce(8)
# c = Territory()
# c.setOwner("Black")
# c.reinforce(6)
# while b.armySize > 3 and c.armySize > 3:
	# b.attack(c, 3)
	# print "b:", b.armySize, "c:", c.armySize

# d = Map(validColors)
# d.territories["Nova York"].setOwner("White")
# d.territories["Nova York"].reinforce(3)
# d.territories["Ottawa"].setOwner("White")
# d.territories["Ottawa"].reinforce(1)
# d.territories["Labrador"].setOwner("White")
# d.relocate("Nova York", "Ottawa", 3)
# d.relocate("Ottawa", "Labrador", 2)
# change it to 3 and you'll get an assertion error :-)

game = Game()
game.addPlayer(Player("White"))
game.addPlayer(Player("Blue"))
game.setup()
game.start()