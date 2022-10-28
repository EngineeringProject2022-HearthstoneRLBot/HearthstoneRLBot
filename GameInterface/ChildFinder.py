from copy import deepcopy

import numpy as np
from fireplace.exceptions import GameOver

import Configuration
from GameInterface import checkValidActionsSparse, interpretDecodedAction, decodeAction, playTurnSparse
from GameState import InputBuilder
from Montecarlo.node import Node
from Benchmark import tt
from Montecarlo.random_node import RandomNode


class ChildFinder:
    def createInput(self, node):
        tt('Input', 1)
        x = InputBuilder.convToInput(node.game)
        tt('Input')
        return x

    def merge(self, node, input):
        if node.randomSample:
            merged = node.parent.merge(node, input)
            if merged:
                return True
        return False

    def predict(self, node, montecarlo, input):
        tt('Model', 1, 6)
        expert_policy_values, network_value = montecarlo.model(input)
        tt('Model')
        arr = expert_policy_values
        node.cached_network_value = network_value
        return arr, node.cached_network_value

    def makeMove(self, node):
        tt('Deepcopy', 1, 6)
        tt('Play turn', 1, 6)
        tt('Adding random', 1, 6)
        tt('Deepcopy')
        tt('Play turn')
        tt('Adding random')
        node.player_number = 1 if node.game.current_player is node.game.player1 else 2
        if node.state is None or node.parent is None or node.finished: #jesli node parent to none to znaczy ze sync byl wiec nie gramy tej tury
            return
        tt('Deepcopy', 1, 6)
        parent = node.parent
        if not node.realGame:
            node.game = deepcopy(node.game)
            node.realGame = True
        tt('Deepcopy')
        is_random = 0
        tt('Play turn', 1, 6)
        try:
            is_random = playTurnSparse(node.game, node.state)
        except GameOver:
            node.finished = True
        tt('Play turn')
        node.player_number = 1 if node.game.current_player is node.game.player1 else 2
        tt('Adding random', 1, 6)
        if is_random and type(parent) is not RandomNode:
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
                randomNode.add_sample(child)
            tt('Adding random')

    def find(self, node, montecarlo):
        tt('Make Move', 1, 5)
        self.makeMove(node)
        tt('Make Move')

        tt('Predicting', 1, 5)
        if node.cached_network_value:
            expert_policy_values, win_value = [], node.cached_network_value
        else:
            nn_input = self.createInput(node)
            merged = self.merge(node, nn_input)
            if merged:
                return True
            expert_policy_values, win_value = self.predict(node, montecarlo,nn_input)
        tt('Predicting')

        tt('Adding node in CF', 1, 5)
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
        tt('Adding node in CF')
        tt('Update WV', 1, 5)
        if node.parent is not None:
            node.cached_initial_win_value = win_value
            node.update_win_value(win_value)
        tt('Update WV')
        return False
