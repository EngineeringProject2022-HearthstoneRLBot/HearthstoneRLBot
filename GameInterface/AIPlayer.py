from copy import deepcopy

from GameInterface import *
import tensorflow as tf

from GameInterface import ChildFinder
from GameState import InputBuilder
import Configuration
from Montecarlo.montecarlo import MonteCarlo
from Montecarlo.node import Node

class AIPlayer(PlayerInterface):
    def __init__(self, name, hero, deck, model_name, simulations, print=True):
        super().__init__(name, hero, deck, print)
        model = tf.keras.models.load_model(f"./Model/models/{model_name}")
        self.model = model
        self.simulations = simulations


    def joinGame(self, game):
        super().joinGame(game)
        montecarlo = MonteCarlo(Node(game), self.model)
        montecarlo.child_finder = ChildFinder.ChildFinder()
        montecarlo.root_node.player_number = 1 if self.game.current_player is self.game.player1 else 2
        montecarlo.player_number = 1 if self.name == self.game.player1.name else 2
        self.montecarlo = montecarlo


    def getPreferredAction(self):
        tt('Preferred->Simulate', 1, 3)
        self.montecarlo.simulate(self.simulations)
        tt('Preferred->Simulate')
        return self.montecarlo.make_exploratory_choice().state

    def getProbabilities(self):
        return self.montecarlo.get_probabilities()

    def sync(self, game, action, isRandom):
        self.montecarlo.sync_tree(game, action)
        self.montecarlo.root_node.parent = None
