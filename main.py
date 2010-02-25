#!/usr/bin/python
# coding: utf-8
from game import Game
from player import Player
from territory import Territory
from map import Map
from card import Card
from globals import validColors

w = Player("White")
w.receiveCard(Card("Brasil", "Triangle"))
w.receiveCard(Card("Argentina", "Square"))
game = Game("map.json", True)
game.addPlayer(w)
game.addPlayer(Player("Blue"))
game.start()
print w
