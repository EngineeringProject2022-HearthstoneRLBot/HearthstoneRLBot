from copy import deepcopy

from GameInterface import *
import tensorflow as tf
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
        montecarlo.child_finder = AIPlayer.child_finder
        montecarlo.root_node.player_number = 1 if self.game.current_player is self.game.player1 else 2
        montecarlo.player_number = 1 if self.game.player1.name == self.name else 2
        self.montecarlo = montecarlo

    def getPreferredAction(self):
        self.montecarlo.simulate(self.simulations)
        if self.montecarlo.make_exploratory_choice().state == 251:
            a = 'a'
        return self.montecarlo.make_exploratory_choice().state

    def getProbabilities(self):
        return self.montecarlo.get_probabilities()

    def sync(self, game, action, isRandom):
        self.montecarlo.sync_tree(game, action, isRandom)
        self.montecarlo.root_node.parent = None


    @staticmethod
    def child_finder(node, montecarlo):
        # node.game.current_player.discard_hand()
        if node.game.current_player.hero.health == 0 and node.game.current_player.opponent.hero.health == 1:
            a = "a"
        # if we have 50 simulations, and after doing 35 we have reached an end node, we are going to "explore this node 15
        # times. This is necessary and good(a win or loss updates our win value average 15 times.) However, the value isn't
        # going to change so we can just cache this value
        if not node.cached_network_value:
            x = InputBuilder.convToInput(node.game)
            expert_policy_values, network_value = montecarlo.model(x)
            win_value = network_value
            node.cached_network_value = network_value
        else:
            win_value = node.cached_network_value

        if montecarlo.player_number != node.player_number:
            win_value *= -1

        # node.win_value = win_value

        # if a node is finished, we know it has no children beacuse it's a game state where the game is actually over.
        # all we have to do is propagate the win value upwards
        if node.finished:
            pass
        else:
            for action in checkValidActionsSparse(node.game):
                child = Node(deepcopy(node.game))
                child.state = action
                child.stateText = (
                            "Action:" + str(action) + " - " + interpretDecodedAction(decodeAction(action), node.game))
                is_random = 0
                try:
                    is_random = playTurnSparse(child.game, action)
                except GameOver:
                    child.finished = True
                child.player_number = 1 if child.game.current_player is child.game.player1 else 2
                child.policy_value = expert_policy_values[0, action]
                if is_random:
                    child.policy_value /= Configuration.RANDOM_MOVE_SAMPLES
                node.add_child(child)
                if is_random:
                    for i in range(Configuration.RANDOM_MOVE_SAMPLES - 1):
                        child = Node(deepcopy(node.game))
                        child.state = action
                        try:
                            playTurnSparse(child.game, action)
                        except GameOver:
                            child.finished = True
                        child.player_number = 1 if child.game.current_player is child.game.player1 else 2
                        child.policy_value = expert_policy_values[0, action] / Configuration.RANDOM_MOVE_SAMPLES
                        node.add_child(child)
        if node.parent is not None:
            node.update_win_value(float(win_value))


