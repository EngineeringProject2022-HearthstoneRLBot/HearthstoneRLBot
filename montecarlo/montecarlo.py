import random
from copy import deepcopy

from GameState import InputBuilder
from montecarlo.node import Node
import numpy as np

class MonteCarlo:

    def __init__(self, root_node, model=None):
        self.root_node = root_node
        self.child_finder = None
        self.node_evaluator = lambda child, montecarlo: None

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
        for i in range(expansion_count):
            current_node = self.root_node
            while current_node.expanded:
                current_node = current_node.get_preferred_child()

            self.expand(current_node)

    def expand(self, node):
        self.child_finder(node, self)
        if len(node.children):
            node.expanded = True

    def sync_tree(self, game, move, is_random: int):
        found = False
        # orientation doesn't matter as long as its the same for both here, as we are only going to look at the board, not hands
        currInput = InputBuilder.convToInput(game, 1)
        for x in self.root_node.children:
            if x.state == move:
                # we found a child with the same move, but it could be a different random state if is_random, so we gta compare boards
                if is_random == 0 or (is_random == 1 and (currInput[:, :, :, 1:3] == InputBuilder.convToInput(x.game, 1)[:, :, :, 1:3]).all()):
                    self.root_node = x
                    if self.root_node.expanded and self.root_node.visits != 0:
                        self.root_node.visits -= 1
                    found = True
                    break
        if not found:
            child = Node(deepcopy(game))
            child.state = move
            child.player_number = child.game.current_player.entity_id - 1
            self.root_node.add_child(child)
            self.root_node = child



    # ### Below Function is created entirely by us
    # def non_user_expand(self, move, callingPlayer):
    #     found = False
    #     for x in self.root_node.children:
    #         if x.state.moves[-1] == move:
    #             self.root_node = x
    #             if self.root_node.original_player is not None:
    #                 if self.root_node.visits[(self.root_node.original_player)-1] != 0:
    #                     self.root_node.visits[(self.root_node.original_player)-1] -= 1
    #             found = True
    #             break
    #     if not found:
    #         child = Node(deepcopy(self.root_node.state))
    #         child.state.move(move)
    #         child.player_number = child.state.whose_turn()
    #         self.root_node.add_child(child)
    #         self.root_node = child
    # ###