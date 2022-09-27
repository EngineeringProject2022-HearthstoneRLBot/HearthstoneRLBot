from GameInterface import *


class DecoratedGame(ModeledGame):

    def __init__(self, player1, player2, startGameEffs=[], startTurnEffs=[], log = False):
        super().__init__(player1, player2, log)
        self.startGameEffs = startGameEffs
        self.startTurnEffs = startTurnEffs

    def startGame(self):
        for eff in self.startGameEffs:
            eff.run(self.game)
        return super().startGame()

    def startTurn(self):
        for eff in self.startTurnEffs:
            eff.run(self.game)
        return super().startTurn()


class GameEffect:
    def run(self, game):
        pass


class GEDealDmg(GameEffect):
    def __init__(self, dmg=28, dmg2=None):
        self.dmg = dmg
        self.dmg2 = dmg if dmg2 is None else dmg2

    def run(self, game):
        for i in range(self.dmg):
            moon = game.player1.give("CS2_008")
            moon.play(target = game.player1.hero)
        for i in range(self.dmg2):
            moon = game.player1.give("CS2_008")
            moon.play(target = game.player2.hero)


class GESetMana(GameEffect):
    def __init__(self, m=10, m2=None):
        self.m = m
        self.m2 = m if m2 is None else m2

    def run(self, game):
        game.player1.max_mana = self.m
        game.player2.max_mana = self.m2


class GEDiscard(GameEffect):
    def __init__(self, p=True, p2=None):
        self.p = p
        self.p2 = p if p2 is None else p2

    def run(self, game):
        if self.p:
            game.player1.discard_hand()
        if self.p2:
            game.player2.discard_hand()


class GERemoveDeck(GameEffect):
    def __init__(self, p=True, p2=None):
        self.p = p
        self.p2 = p if p2 is None else p2

    def run(self, game):
        if self.p:
            game.player1.deck = []
        if self.p2:
            game.player2.deck = []


class GEEndTurn(GameEffect):
    def run(self, game):
        game.end_turn()

