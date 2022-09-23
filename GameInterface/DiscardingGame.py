from ModeledGame import ModeledGame

class DiscardingGame(ModeledGame):
    def beforeStart(self):
        self.game.player1.max_mana = 10
        self.game.player2.max_mana = 10
        for i in range(28):
            moon = self.game.player1.give("CS2_008")
            moon.play(target=self.game.player1.hero)
        self.game.end_turn()
        for i in range(28):
            moon = self.game.player2.give("CS2_008")
            moon.play(target=self.game.player2.hero)
        self.game.player1.discard_hand()
        self.game.player2.discard_hand()
        self.game.player1.deck = []
        self.game.player2.deck = []
        self.player1.joinGame(self.game)
        self.player2.joinGame(self.game)

    def startTurn(self):
        self.game.current_player.discard_hand()