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
            moon = game.current_player.give("CS2_008")
            moon.play(target = game.current_player.hero)
        for i in range(self.dmg2):
            moon = game.current_player.give("CS2_008")
            moon.play(target = game.current_player.opponent.hero)


class GESetMaxMana(GameEffect):
    def __init__(self, m=10, m2=None):
        self.m = m
        self.m2 = m if m2 is None else m2

    def run(self, game):
        game.current_player.max_mana = self.m
        game.current_player.opponent.max_mana = self.m2


class GEDiscard(GameEffect):
    def __init__(self, p=True, p2=None):
        self.p = p
        self.p2 = p if p2 is None else p2

    def run(self, game):
        if self.p:
            game.current_player.discard_hand()
        if self.p2:
            game.current_player.opponent.discard_hand()


class GERemoveDeck(GameEffect):
    def __init__(self, p=True, p2=None):
        self.p = p
        self.p2 = p if p2 is None else p2

    def run(self, game):
        if self.p:
            game.current_player.deck = []
        if self.p2:
            game.current_player.opponent.deck = []


class GEEndTurn(GameEffect):
    def run(self, game):
        game.end_turn()

# still being tested and developed
# coin : GAME_005
class GEPlayMinionTimes(GameEffect):
    def __init__(self, cards):
        self.cards = cards

    def run(self, game):
        p = game.current_player
        for tuple in self.cards:
            for j in range(0, tuple[1]):
                cardToBePlayed = p.give(tuple[0])
                while(cardToBePlayed.cost > p.mana):
                    coin = p.give('GAME_005')
                    coin.play()
                cardToBePlayed.play()

class GEGiveCards(GameEffect):
    def __init__(self, cardsP1 = [], cardsP2 = []):
        if cardsP1 == []:
            self.cardsP1 = []
        else:
            self.cardsP1 = cardsP1

        if cardsP2 == []:
            self.cardsP2 = []
        else:
            self.cardsP2 = cardsP2


    def run(self, game):
        p1 = str(game.player1)[0]
        if p1 != "1":
            p1 = game.player2
            p2 = game.player1
        else:
            p1 = game.player1
            p2 = game.player2

            for tuple in self.cardsP1:
                for j in range(0, tuple[1]):
                    p1.give(tuple[0])
            for tuple in self.cardsP2:
                for j in range(0, tuple[1]):
                    p2.give(tuple[0])

class GESetStarterPlayer(GameEffect):
    def __init__(self, player):
        self.player = str(player)

    def run(self, game):
        p1 = str(game.player1)[0]
        if p1 != self.player:
            game.end_turn()
        else:
            pass