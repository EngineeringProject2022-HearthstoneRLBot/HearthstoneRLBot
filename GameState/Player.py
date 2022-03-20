class Player:
    def __init__(self):
        self.hero = Hero()
        self.handCards = []
        for i in range(10):
            self.handCards.append(HandCard())
        self.boardCards = []
        for i in range(7):
            self.boardCards.append(BoardCard())