from subprocess import TimeoutExpired

from GameInterface import *

from waiting import wait

class ManualPlayer(PlayerInterface):
    def __init__(self, name, hero, deck, print = True):
        super().__init__(name, hero, deck, print)
        self.input = None

    def play(self):
        self.input = None
        return super().play()

    def isInputReady(self):
        return self.input is not None

    def getPreferredAction(self):
        try:
            wait(self.isInputReady, timeout_seconds=60)
            return self.input
        except TimeoutExpired:
            return 251

    def getProbabilities(self):
        arr = checkValidActions(self.game)
        return arr/sum(arr)