from fireplace.exceptions import GameOver

from GameCommunication import *
from GameConvenience import interpretDecodedAction, decodeAction


class PlayerInterface:
    def __init__(self, name, hero, deck, print = True):
        self.game = None
        self.hero = hero
        self.deck = deck
        self.name = name
        self.print = print

    def play(self):
        action = self.getPreferredAction()
        probabilities = self.getProbabilities()
        if self.print:
            print("Turn: " + str(self.game.turn) + ", Action:" + str(action) + " - ",
                  (interpretDecodedAction(decodeAction(action), self.game)))
        isRandom = False
        try:
            isRandom = playTurnSparse(self.game, action)
        except GameOver:
            pass
        return action, probabilities, isRandom

    def getPreferredAction(self):
        return 251

    def getProbabilities(self):
        return 251*[0]+[1]

    def joinGame(self, game):
        self.game = game

    def sync(self, action, isRandom):
        pass
