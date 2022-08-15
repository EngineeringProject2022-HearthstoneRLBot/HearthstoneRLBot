import math
import pickle
import random
from math import log, sqrt


class NoChildException(Exception):
    pass


class Node:

    def __init__(self, game):
        self.state = None
        self.game = game
        self.win_value = 0
        self.policy_value = None
        self.visits = 0
        self.parent = None
        self.children = []
        self.expanded = False
        self.player_number = None
        self.discovery_factor = 1
        ### below code is added by us
        self.finished = False
        ###

    def update_win_value(self, value):
        ### below code is modified by us
        newValue = value
        multiplier = 1
        if self.visits != 0:
            sum = self.win_value * self.visits
            sum += (newValue * multiplier)
            newValue = sum / (self.visits + 1)

        self.win_value = newValue
        self.visits += 1
        if self.parent:
            self.parent.update_win_value(value)
        ###

    def update_policy_value(self, value):
        self.policy_value = value

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def get_preferred_child(self):
        best_children = []
        best_score = float('-inf')

        for child in self.children:
            score = 0
            numbers = 0
            for child_2 in self.children:
                if child_2.state == child.state:
                    score += child.get_score()
                    numbers += 1
            # score = child.get_score(callingPlayer)
            score = score / numbers
            if score > best_score:
                best_score = score
                best_children = [child]
            elif score == best_score:
                best_children.append(child)
        try:
            return random.choice(best_children)
        except IndexError:
            raise NoChildException

    def get_score(self):
        ###Below code is modified by us
        # if self.finished:
        #     # who won?
        #     if self.game.current_player.playstate is PlayState.WON:
        #         self.win_value = 1
        #     else:
        #         self.win_value = -1
        if not self.expanded:
            # or self.visits[callingPlayer -1] < 6:
            discovery_operand = float('inf')
            win_operand = 0
        else:
            discovery_operand = self.discovery_factor * (self.policy_value or 1) * (
                        (sqrt(self.parent.visits)) / (1 + self.visits))
            win_multiplier = 1
            win_operand = win_multiplier * self.win_value
        self.score = win_operand + discovery_operand
        return self.score
        ###
