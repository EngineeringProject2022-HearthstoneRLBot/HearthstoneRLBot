import random

from GameCommunication import checkValidActionsSparse, checkValidActions
from GameInterface import PlayerInterface


class RandomPlayer(PlayerInterface):
    def getPreferredAction(self):
        actions = checkValidActionsSparse(self.game)
        return random.choice(actions)

    def getProbabilities(self):
        arr = checkValidActions(self.game)
        return arr/sum(arr)