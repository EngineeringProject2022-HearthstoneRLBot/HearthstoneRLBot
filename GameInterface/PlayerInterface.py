from GameCommunication import *


class PlayerInterface:
    def __init__(self, name, hero, deck):
        self.game = None
        self.hero = hero
        self.deck = deck
        self.name = name

    def play(self):
        playTurnSparse(self.game, self.getPreferredAction())

    def getPreferredAction(self):
        return 251

    def joinGame(self, game):
        self.game = game
