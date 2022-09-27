import random

from GameInterface import *


class RandomPlayer(PlayerInterface):
    def getPreferredAction(self):
        actions = checkValidActionsSparse(self.game)
        return random.choice(actions)

    def getProbabilities(self):
        arr = checkValidActions(self.game)
        return arr/sum(arr)