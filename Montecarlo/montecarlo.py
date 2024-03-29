import random
from copy import deepcopy

from Benchmark import tt
import Configuration
from GameState import InputBuilder
from Montecarlo.node import Node
import numpy as np


class MonteCarlo:

    def __init__(self, root_node, model=None):
        self.root_node = root_node
        self.child_finder = None
        self.node_evaluator = lambda child, montecarlo: None
        self.player_number = None
        ###Below Code is created by us
        self.model = model
        ###

    def make_choice(self):
        self.root_node.active = False
        best_children = []
        most_visits = float('-inf')

        for child in self.root_node.children:
            if child.visits > most_visits:
                most_visits = child.visits
                best_children = [child]
            elif child.visits == most_visits:
                best_children.append(child)
        theChoice = random.choice(best_children)
        theChoice.parent = None
        return theChoice

    ###Below Function is created entirely by us
    def get_probabilities(self):
        moves = np.zeros(252)
        for child in self.root_node.children:
            if self.root_node.visits == 0:
                moves[child.state] = 1
            else:
                moves[child.state] = child.visits / self.root_node.visits
        # children_visits = map(lambda child:  child.visits[callingPlayer-1], self.root_node.children)
        # children_visit_probabilities = [visit / self.root_node.visits[callingPlayer-1] for visit in children_visits]
        return moves

    ###

    def make_exploratory_choice(self):
        self.root_node.active = False
        children_visits = map(lambda child: child.visits, self.root_node.children)
        # l = list(map(lambda child: child.win_value, self.root_node.children))   ###
        # return self.root_node.children[l.index(max(l))]                         ###
        children_visit_probabilities = [visit / self.root_node.visits for visit in children_visits]
        sum_probs = sum(children_visit_probabilities)
        if sum_probs != 1.0:
            children_visit_probabilities[-1] += (1.0 - sum_probs)
        random_probability = random.uniform(0, 1)
        probabilities_already_counted = 0.

        for i, probability in enumerate(children_visit_probabilities):
            if probabilities_already_counted + probability >= random_probability:
                # self.root_node.children[i].parent = None
                return self.root_node.children[i]

            probabilities_already_counted += probability

    def simulate(self, expansion_count=1):
        i = 0

        while i < expansion_count:
            failure = True

            while failure:
                if self.root_node.expanded and len(self.root_node.children) == 1 and self.root_node.children[
                    0].expanded:
                    # value of visits doesn't matter here(and for training we save distribution which will always be the
                    # same because 100% to one child. No matter how many visits, it will always be selected
                    # the one visit to parent is just cosmetic(parent 0 visits child 1 visit would look strange)
                    print("shortcut")
                    return
                tt('Searching for node', 1, 4)
                current_node = self.root_node
                while current_node.expanded:
                    current_node = current_node.get_preferred_child(self.player_number)
                tt('Searching for node')
                tt('Expansion', 1, 4)
                failure = self.expand(current_node)
                tt('Expansion')

            i += 1

            if expansion_count < Configuration.MCTS_CHILD_MULTIPLIER * len(self.root_node.children):
                expansion_count = Configuration.MCTS_CHILD_MULTIPLIER * len(self.root_node.children)

    def expand(self, node):

        failure = self.child_finder.find(node, self)
        if len(node.children):
            node.expanded = True
        return failure

    def sync_tree(self, game, move):
        found = False
        currInput = InputBuilder.convToInput(game, self.player_number)
        children = [x for x in self.root_node.children if x not in self.root_node.randomChildren]
        for randomChild in self.root_node.randomChildren:
            children.extend([x[0] for x in randomChild.samples])
        for x in children:
            if not x.realGame:
                continue
            if (1 if game.current_player is game.player1 else 2) != x.player_number:
                # if (InputBuilder.convToInput(x.game, self.player_number) == currInput).all():
                #     print("would have synced to enemy")
                continue

            child_input = InputBuilder.convToInput(x.game, self.player_number)

            if (currInput == child_input).all():
                self.root_node = x
                if self.root_node.expanded and self.root_node.visits != 0:
                    self.root_node.visits -= 1
                found = True
                break
        if not found:
            child = Node(game)
            child.state = move
            child.player_number = 1 if child.game.current_player is child.game.player1 else 2
            self.root_node.add_child(child)
            self.root_node = child
