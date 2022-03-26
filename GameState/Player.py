from .Hero import Hero
from .HandCards import HandCard
from .BoardCards import BoardCard


class Player:
    def __init__(self, state, playerNumber):
        self.playerNumber = playerNumber;
        self.hero = Hero()
        self.handCards = []
        for card in state.hands:
            if card.controller.name == "Player"+str(self.playerNumber):
                self.handCards.append(HandCard(card))
#        for i in range(10):
#            self.handCards.append(HandCard())
        self.boardCards = []
#        for i in range(7):
#            self.boardCards.append(BoardCard())
