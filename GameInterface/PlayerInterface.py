from fireplace.exceptions import GameOver

from Benchmark import tt
from GameInterface import *

class PlayerInterface:
    def __init__(self, name, hero, deck, print = True):
        self.game = None
        self.hero = hero
        self.deck = deck
        self.name = name
        self.print = print

    def play(self):
        tt('Action', 1, 2)
        action = self.getPreferredAction()
        tt('Action')
        tt('Probs', 1, 2)
        probabilities = self.getProbabilities()
        tt('Probs')
        tt('Print&Play', 1, 2)
        if self.print:
            print(self.name + " Turn: " + str(self.game.turn) + ", Action:" + str(action) + " - ",
                  (interpretDecodedAction(decodeAction(action), self.game)))
        isRandom = False
        try:
            isRandom = playTurnSparse(self.game, action)
        except GameOver:
            pass
        tt('Print&Play')
        return action, probabilities, isRandom

    def getPreferredAction(self):
        return 251

    def getProbabilities(self):
        return 251*[0]+[1]

    def joinGame(self, game):
        self.game = game

    def sync(self, game, action, isRandom):
        pass
