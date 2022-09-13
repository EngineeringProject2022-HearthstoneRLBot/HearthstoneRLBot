from fireplace.exceptions import GameOver
from fireplace.game import Game
from fireplace.player import Player
from hearthstone.enums import CardClass

from GameSetupUtils import mulliganRandomChoice
from GameState import InputBuilder


class ModeledGame:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        game = Game(players=(self.createPlayer(player1),
                             self.createPlayer(player2)))
        game.start()
        mulliganRandomChoice(game)
        self.game = game
        self.winner = None
        self.gameData = []
        self.player1.joinGame(game)
        self.player2.joinGame(game)

    def createPlayer(self, player):
        return Player(player.name, player.deck, CardClass(player.hero).default_hero)

    def start(self):
        self.data.append((self.player1.hero, self.player1.deck, self.player2.hero, self.player2.deck))
        while True:
            data = InputBuilder.convToInput(self.game)
            player = 1 if self.game.current_player is self.game.player1 else 2
            try:
                action, probabilities = self.playTurn()
            except:
            self.data.append((data, probabilities, player, action)) #to wcześniej było przed wykonaniem ruchu co teraz

    def playTurn(self):
        if self.game.current_player.name == self.player1.name:
            return self.player1.play() #tu zwroty muszą być
        else:
            return self.player2.play()
