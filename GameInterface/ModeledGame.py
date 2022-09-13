import numpy as np
from fireplace.exceptions import GameOver
from fireplace.game import Game
from fireplace.player import Player
from fireplace import logging
from hearthstone.enums import CardClass, PlayState

from GameConvenience import interpretDecodedAction, decodeAction
from GameSetupUtils import mulliganRandomChoice
from GameState import InputBuilder


class ModeledGame:
    def __init__(self, player1, player2, log = False):
        logger = logging.log
        logger.disabled = not log
        logger.propagate = log

        self.player1 = player1
        self.player2 = player2
        game = Game(players=(self.createPlayer(player1),
                             self.createPlayer(player2)))
        game.start()
        mulliganRandomChoice(game)
        self.game = game
        self.winner = None
        self.data = []
        self.player1.joinGame(game)
        self.player2.joinGame(game)


    def createPlayer(self, player):
        return Player(player.name, player.deck, CardClass(player.hero).default_hero)

    def start(self):
        self.data.append((self.player1.hero, self.player1.deck,
                          self.player2.hero, self.player2.deck,
                          self.game.player1.name, self.game.player2.name))  # dodałem zapisywanie nazw dzięki
                                                                            # czemu ustawiając je np na
                                                                            # HunterStupidD1, MageIntelligentD3
                                                                            # będziemy wiedzieli, że np
                                                                            # player1 to jest głupi hunter, a
                                                                            # player2 to inteligentny mag xD
                                                                            # można ustawić dowolne nazwy co też pozwoli
                                                                            # grać np HunterIteration1 vs HunterIteration2
                                                                            # i ich odróżniać (nie tylko na pdostawie deck)
                                                                            # wg mnie to daje więcej swobody niż
                                                                            # zapisywanie typu klasy, hero i decka samego
        while True:
            data = InputBuilder.convToInput(self.game)
            player = 1 if self.game.current_player is self.game.player1 else 2
            action, probabilities, isRandom = self.playTurn()
            self.sync(action, isRandom)
            self.data.append((data, probabilities, player, action))

            if self.gameFinished():
                break

        self.data.append((InputBuilder.convToInput(self.game), np.zeros(252),
                          1 if self.game.current_player is self.game.player1 else 2, None))
        print('Game Finished! :)')

    def playTurn(self):
        if self.game.current_player.name == self.player1.name:
            return self.player1.play()
        else:
            return self.player2.play()

    def sync(self, action, isRandom):
        self.player1.sync(action, isRandom)
        self.player2.sync(action, isRandom)

    def gameFinished(self):
        if self.game.player1.playstate is PlayState.WON:
            winner = 1
            return True
        if self.game.player2.playstate is PlayState.WON:
            winner = 2
            return True
        if self.game.ended:
            winner = 3
            return True
        return False
