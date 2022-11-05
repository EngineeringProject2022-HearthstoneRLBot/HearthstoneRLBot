import Benchmark
from GameInterface import *
from fireplace.game import Game
from fireplace.player import Player
from fireplace import logging
from hearthstone.enums import CardClass, PlayState

from GameState import InputBuilder

from Benchmark import tt
from MultiThreading.PrintQueue import PrintQueue


class ModeledGame:
    def __init__(self, player1, player2, log=False):
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
        self.startGame()
        totalTurn = 0
        a = np.zeros(252)
        a.fill(1/252)
        while True:
            tt('Full turn', 1)
            self.startTurn()

            player = 1 if self.game.current_player is self.game.player1 else 2
            data = InputBuilder.convToInput(self.game, player)
            player2 = 2 if player == 1 else 1
            data2 = InputBuilder.convToInput(self.game, player2)
            tt('RealPlay', 1, 1)
            action, probabilities, isRandom = self.playTurn()
            tt('RealPlay')
            tt('Sync', 1, 1)
            self.sync(action, isRandom)
            tt('Sync')
            self.data.append((data, probabilities, player, action))

            self.data.append((data2, a, player2, action))
            tt('Full turn')

            Benchmark.printTimers()

            if self.gameFinished():
                break

        player = 1 if self.game.current_player is self.game.player1 else 2
        self.data.append((InputBuilder.convToInput(self.game, player), a,
                          player, None))
        player2 = 2 if player == 1 else 1
        self.data.append((InputBuilder.convToInput(self.game, player2), a,
                          player2, None))

        if self.winner == 1:
            PrintQueue.add(f'Game Finished! :) Player {self.game.player1.name} won!')
        elif self.winner == 2:
            PrintQueue.add(f'Game Finished! :) Player {self.game.player2.name} won!')
        else:
            PrintQueue.add(f'Game Finished! :( Couldn\'t find a winner')

    def playTurn(self):
        if self.game.current_player.name == self.player1.name:
            return self.player1.play()
        else:
            return self.player2.play()

    def sync(self, action, isRandom):
        self.player1.sync(self.game, action, isRandom)
        self.player2.sync(self.game, action, isRandom)

    def gameFinished(self):
        if self.game.player1.playstate is PlayState.WON:
            self.winner = 1
            return True
        if self.game.player2.playstate is PlayState.WON:
            self.winner = 2
            return True
        if self.game.ended:
            self.winner = 3
            return True
        return False

    def prepareGamersData(self):
        # Moim zdaniem to nie ma tak, że dobrze albo że nie dobrze. Gdybym miał powiedzieć, co cenię w życiu najbardziej,
        # powiedziałbym, że ludzi. Ekhm… Ludzi, którzy podali mi pomocną dłoń, kiedy sobie nie radziłem, kiedy byłem sam.
        # I co ciekawe, to właśnie przypadkowe spotkania wpływają na nasze życie. Chodzi o to, że kiedy wyznaje się
        # pewne wartości, nawet pozornie uniwersalne, bywa, że nie znajduje się zrozumienia, które by tak rzec, które
        # pomaga się nam rozwijać. Ja miałem szczęście, by tak rzec, ponieważ je znalazłem. I dziękuję życiu. Dziękuję
        # mu, życie to śpiew, życie to taniec, życie to miłość. Wielu ludzi pyta mnie o to samo, ale jak ty to robisz?
        # Skąd czerpiesz tę radość? A ja odpowiadam, że to proste, to umiłowanie życia, to właśnie ono sprawia, że
        # dzisiaj na przykład buduję maszyny, a jutro… kto wie, dlaczego by nie, oddam się pracy społecznej i
        # będę ot, choćby sadzić… znaczy… marchew.

        # Dodałem tu self.player1.name aby później sobie zmapować kto zaczynał
        # Z poczatku myslalem, że ustawię po prostu player1 i player2 i na tej podstawie będę dawał info o tym
        # Kto wygrał (czy nasz ustalony player1 czy nasz ustalony player2) no ale wtedy byśmy stracili info
        # Kto zaczynał (więc to było błędne w starym GamePlayerze, ale nie używane to nie wyszło)
        return (self.player1.name, self.player1.hero, self.player1.deck,
                self.player2.name, self.player2.hero, self.player2.deck,
                self.game.player1.name, self.game.player2.name)

    def startTurn(self):
        pass

    def startGame(self):
        pass
