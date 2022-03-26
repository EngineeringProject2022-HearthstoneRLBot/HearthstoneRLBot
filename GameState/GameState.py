from .Player import Player


class GameState:
    def __init__(self, state):
        self.players = []
        for i in range(2):
            self.players.append(Player(state, i+1))

       #for player in self.players:
