from copy import deepcopy

from fireplace.exceptions import GameOver

import Configuration
from GameInterface import checkValidActionsSparse, interpretDecodedAction, decodeAction, playTurnSparse
from GameState import InputBuilder
from Montecarlo.node import Node
from Benchmark import tt

class ChildFinder:

    def predict(self, node, montecarlo):
        if node.cached_network_value:
            return [], node.cached_network_value

        tt('Input', 1)
        x = InputBuilder.convToInput(node.game)
        tt('Input')
        tt('Model', 1)
        expert_policy_values, network_value = montecarlo.model(x)
        tt('Model')
        node.cached_network_value = network_value
        return expert_policy_values, network_value

    def makeMove(self, node):
        node.player_number = 1 if node.game.current_player is node.game.player1 else 2
        if node.state is None or node.parent is None or node.finished: #jesli node parent to none to znaczy ze sync byl wiec nie gramy tej tury
            return
        if not node.realGame:
            tt('Deepcopy', 1)
            node.game = deepcopy(node.game)
            tt('Deepcopy')
            node.realGame = True
        is_random = 0
        tt('Play turn', 1)
        try:
            is_random = playTurnSparse(node.game, node.state)
        except GameOver:
            node.finished = True
        tt('Play turn')
        node.player_number = 1 if node.game.current_player is node.game.player1 else 2

        if is_random and node.propagate:
            node.policy_value /= Configuration.RANDOM_MOVE_SAMPLES
            for i in range(Configuration.RANDOM_MOVE_SAMPLES - 1):
                child = Node(node.parent.game)
                child.state = node.state
                child.stateText = (
                        "Duplicate Random Action:" + str(child.state) + " - " + interpretDecodedAction(decodeAction(child.state), child.game))
                child.policy_value = node.policy_value
                child.propagate = False
                node.parent.add_child(child)


    def predictHand(self, node, montecarlo):
        if montecarlo.player_number == node.player_number:
            toMask = node.game.current_player.opponent
        else:
            toMask = node.game.current_player
        cardCount = len(toMask.hand)
        toMask.discard_hand()
        for i in range(cardCount):
            toMask.give("FP1_012")

    def find(self, node, montecarlo):
        tt('Total CF', 1)
        self.makeMove(node)
        if node.parent is not None and not node.finished: # ROOT NODE
            self.predictHand(node, montecarlo)
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
                child.player_number = 1 if node.game.current_player is node.game.player1 else 2
                node.add_child(child)

        if node.parent is not None:
            node.update_win_value(win_value)
        tt('Total CF')
