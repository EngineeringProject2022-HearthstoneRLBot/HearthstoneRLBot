from copy import deepcopy

from fireplace.exceptions import GameOver

import Configuration
from GameInterface import checkValidActionsSparse, interpretDecodedAction, decodeAction, playTurnSparse
from GameState import InputBuilder
from Montecarlo.node import Node
from Benchmark import tt
from Montecarlo.random_node import RandomNode


class ChildFinder:

    def predict(self, node, montecarlo):
        if node.cached_network_value:
            return [], node.cached_network_value

        tt('Input', 1)
        x = InputBuilder.convToInput(node.game)
        tt('Input')
        if node.randomSample:
            merged = node.parent.merge(node, x)
            if merged is not None:
                return None, None
        tt('Model', 1)
        expert_policy_values, network_value = montecarlo.model(x)
        tt('Model')
        node.cached_network_value = network_value
        return expert_policy_values, network_value

    def makeMove(self, node):
        node.player_number = 1 if node.game.current_player is node.game.player1 else 2
        if node.state is None or node.parent is None or node.finished: #jesli node parent to none to znaczy ze sync byl wiec nie gramy tej tury
            return
        parent = node.parent
        if not node.realGame:
            tt('Deepcopy', 1)
            node.game = deepcopy(parent.game)
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

        # is_random = int(input())
        is_random = True
        if is_random == 1 and type(parent) is not RandomNode:

            randomNode = RandomNode(node, parent.game)
            node.stateText = "RANDOM MOVE SAMPLE: " + node.stateText
            parent.randomChildren.append(randomNode)
            node.randomSample = True
            node.parent = randomNode
            parent.children.remove(node)
            parent.add_child(randomNode)
            randomNode.expanded = True
            for i in range(Configuration.RANDOM_MOVE_SAMPLES - 1):
                child = Node(parent.game)
                child.randomSample = True
                child.parent = randomNode
                child.state = node.state
                child.stateText = node.stateText
                child.player_number = node.player_number
                #child.propagate = False
                randomNode.add_sample(child)
            pass



    def find(self, node, montecarlo):
        tt('Total CF', 1)
        self.makeMove(node)
        expert_policy_values, win_value = self.predict(node, montecarlo)
        if expert_policy_values is None:
            return False
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
            node.cached_initial_win_value = win_value
            node.update_win_value(win_value)

        tt('Total CF')
        return True
