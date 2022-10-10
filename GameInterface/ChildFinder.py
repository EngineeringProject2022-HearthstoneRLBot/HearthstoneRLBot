from copy import deepcopy

from fireplace.exceptions import GameOver

import Configuration
from GameInterface import checkValidActionsSparse, interpretDecodedAction, decodeAction, playTurnSparse
from GameState import InputBuilder
from Montecarlo.node import Node

from timeit import default_timer as timer

class ChildFinder:

    def predict(self, node, montecarlo):
        if node.cached_network_value:
            return [], node.cached_network_value
        t1 = timer()
        x = InputBuilder.convToInput(node.game)
        t2 = timer()
        Configuration.totalInput += (t2-t1)
        t1 = timer()
        expert_policy_values, network_value = montecarlo.model(x)
        t2 = timer()
        Configuration.totalModel += (t2-t1)
        node.cached_network_value = network_value
        return expert_policy_values, network_value

    def makeMove(self, node):
        node.player_number = 1 if node.game.current_player is node.game.player1 else 2
        if node.state is None or node.parent is None: #jesli node parent to none to znaczy ze sync byl wiec nie gramy tej tury
            return
        t1 = timer()
        node.game = deepcopy(node.game)
        t2 = timer()
        Configuration.totalDC += (t2-t1)
        is_random = 0
        try:
            is_random = playTurnSparse(node.game, node.state)
        except GameOver:
            node.finished = True
        node.player_number = 1 if node.game.current_player is node.game.player1 else 2

        if is_random and node.propagate:
            node.policy_value /= Configuration.RANDOM_MOVE_SAMPLES
            for i in range(Configuration.RANDOM_MOVE_SAMPLES - 1):
                child = Node(node.parent.game)
                child.state = node.state
                child.stateText = (
                        "Action:" + str(child.state) + " - " + interpretDecodedAction(decodeAction(child.state), child.game))
                child.policy_value = node.policy_value
                child.propagate = False
                node.parent.add_child(child)


    def find(self, node, montecarlo):
        t1 = timer()
        self.makeMove(node)
        expert_policy_values, win_value = self.predict(node, montecarlo)
        if montecarlo.player_number != node.player_number:
            win_value *= -1
        if not node.finished:
            for action in checkValidActionsSparse(node.game):
                child = Node(node.game)
                child.state = action
                child.stateText = (
                        "Action:" + str(action) + " - " + interpretDecodedAction(decodeAction(action), node.game))
                child.policy_value = expert_policy_values[0, action]
                child.player_number = node.player_number if child.state != 251 else (not (node.player_number-1))+1
                node.add_child(child)
        if node.parent is not None:
            node.update_win_value(float(win_value))
        t2 = timer()
        Configuration.total += (t2-t1)
