from random import random

from GameCommunication import checkValidActionsSparse
from GameInterface import PlayerInterface


class RandomPlayer(PlayerInterface):
    def getPreferredAction(self):
        actions = checkValidActionsSparse(self.game)
        return random.choice(actions)
