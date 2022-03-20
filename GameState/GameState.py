from .Player import Player


class GameState:
    def __init__(self):
        self.players = []
        for i in range(2):
            self.players.append(Player())
