import random
from copy import deepcopy

from Benchmark import tt
from Montecarlo.node import Node


class RandomNode(Node):

    def __init__(self, node: Node, game):
        super().__init__(game)
        self.player_number = node.player_number
        self.policy_value = node.policy_value
        self.state = node.state
        self.stateText = "Random Node for: " + node.stateText
        self.parent = node.parent
        # node, cached input, probability multiplier
        self.samples = [[node, None, 1]]
        self.children = []

    def add_sample(self, node: Node):
        self.samples.append([node, None, 1])

    def update_win_value(self, value):
        total_win = 0.0
        total_weight = 0.0
        for sample in self.samples:
            total_win += (sample[0].win_value * sample[2]) if sample[0].visits > 0 else 0
            total_weight += sample[2] if sample[0].visits > 0 else 0
        self.win_value = total_win / total_weight
        self.visits += 1
        if self.parent:
            self.parent.update_win_value(value)

    def get_preferred_child(self, callingPlayer):

        probs = [x[2] for x in self.samples]
        chance = sum(probs)
        p_dist = [x / chance for x in probs]
        child = random.choices(population=self.samples, weights=p_dist, k=1)[0][0]
        if child.expanded:
            return child.get_preferred_child(callingPlayer)
        else:
            return child

    def merge(self, node, encoded_state):
        merged = None
        found_self = None
        for x in self.samples:
            if not found_self and x[0] is node:
                x[1] = encoded_state
                found_self = x
            elif not merged and (x[1] == encoded_state).all():
                x[2] = x[2] + 1
                merged = x

        if merged:
            merged[0].visits += found_self[0].visits
            self.samples.remove(found_self)
            return merged
        else:
            return None
