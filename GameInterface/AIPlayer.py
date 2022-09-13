from GameCommunication import playTurnSparse
from GameInterface import PlayerInterface
import tensorflow as tf

from montecarlo.montecarlo import MonteCarlo
from montecarlo.node import Node
from GamePlayer import child_finder


class AIPlayer(PlayerInterface):
    def __init__(self, name, hero, deck, model_name, simulations):
        super().__init__(name, hero, deck)
        model = tf.keras.models.load_model(f"../Model/models/{model_name}")
        self.model = model
        self.simulations = simulations

    def joinGame(self, game):
        super().joinGame(game)
        montecarlo = MonteCarlo(Node(game), self.model)
        montecarlo.child_finder = child_finder
        montecarlo.root_node.player_number = 1 if self.game.current_player is self.game.player1 else 2
        montecarlo.player_number = 1 if self.game.player1.name == self.name else 2
        self.montecarlo = montecarlo

    def getPreferredAction(self):
        self.montecarlo.simulate(self.simulations)
        action = self.montecarlo.make_exploratory_choice().state
        playTurnSparse(self.game, action)

