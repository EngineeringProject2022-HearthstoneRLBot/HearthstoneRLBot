import pickle
import sys
import traceback
from copy import deepcopy
import random

from fireplace.exceptions import GameOver
from fireplace.utils import random_draft
from hearthstone.enums import CardClass, PlayState

from GameCommunication import checkValidActionsSparse, playTurnSparse
from GameSetupUtils import mulliganRandomChoice
from GameState import InputBuilder
from montecarlo.montecarlo import MonteCarlo
from montecarlo.node import Node

RANDOM_MOVE_SAMPLES = 5

def _setup_game(data):
    # we setup our game here
    from fireplace.game import Game
    from fireplace.player import Player

    randomClassOne = random.randrange(2, 10)
    randomClassTwo = random.randrange(2, 10)
    deck1 = random_draft(CardClass(randomClassOne))
    deck2 = random_draft(CardClass(randomClassTwo))
    data.append((randomClassOne, deck1, randomClassTwo, deck2))
    player1 = Player("Player1", deck1, CardClass(randomClassOne).default_hero)
    player2 = Player("Player2", deck2, CardClass(randomClassTwo).default_hero)

    game = Game(players=(player1, player2))
    game.start()
    mulliganRandomChoice(game)
    return game

def playGame(model, simulations, seedObject = None):
    if seedObject != None:
        random.setstate(seedObject)
    data = []
    game = _setup_game(data)
    montecarlo = MonteCarlo(Node(game), model)
    montecarlo.child_finder = child_finder
    montecarlo.root_node.player_number = 1
    winner = 0
    try:
        while True:
            currPlayer = game.current_player.entity_id - 1

            currInput = InputBuilder.convToInput(game, currPlayer)
            montecarlo.simulate(simulations, currPlayer)  # number of simulations per turn. do not put less than 2
            probabilities = montecarlo.get_probabilities(currPlayer)

            montecarlo.root_node = montecarlo.make_exploratory_choice(currPlayer)

            # else:
            #    montecarlo.root_node = montecarlo.make_choice(currPlayer) #rest of moves are the network playing "optimally"

            if montecarlo.root_node.visits[montecarlo.root_node.original_player - 1] != 0:
                montecarlo.root_node.visits[montecarlo.root_node.original_player - 1] -= 1

            # zamieniłem bo chcemy appendować co zrobiliśmy i dopiero wtedy zagrać turę - ten ostatni ruch
            # spowodował naszą wygraną (co nie byłoby zapisane do pliku, bo exception)
            print("Turn: " + str(montecarlo.root_node.parent.game.turn) + ", Action:" + str(montecarlo.root_node.state))

            data.append(((currInput[:, :, :, 0:3], currInput[0, 0, 0, 3]), probabilities, currPlayer,
                             montecarlo.root_node.state))
            playTurnSparse(montecarlo.root_node.parent.game, montecarlo.root_node.state)
            montecarlo.root_node.parent = None
            # if len(game.moves) >= 120:  # game too long, auto-draw
            #     break
    except GameOver as e:
        if montecarlo.root_node.game.player1.playstate is PlayState.WON:
            winner = 1
        elif montecarlo.root_node.game.player2.playstate is PlayState.WON:
            winner = 2
        else:
            winner = 3
    except Exception as e:
        winner = 4
        data.append(traceback.format_exc())
        print(traceback.format_exc())
    return winner, data

def selfplay(model, numbgame, simulations, fileName):
    for i in range(numbgame):
        print("GAME " + str(i+1))
        state = random.getstate()
        winner, data = playGame(model, simulations)
        with open("data/" + fileName + ".txt", "ab") as fp:
            pickle.dump((data, winner, state), fp)


def child_finder(node, montecarlo, simulatingPlayer):
    node.original_player = simulatingPlayer
    if node.finished:
        win_value = 1
    else:
        x = InputBuilder.convToInput(node.game, node.player_number)
        expert_policy_values, win_value = montecarlo.model(x)
        for action in checkValidActionsSparse(node.game):
            child = Node(deepcopy(node.game))
            child.state = action
            is_random = 0
            try:
                is_random = playTurnSparse(child.game, action)
            except GameOver:
                child.finished = True
            child.player_number = child.game.current_player.entity_id - 1
            child.policy_value = expert_policy_values[0, action]
            if is_random:
                child.policy_value /= RANDOM_MOVE_SAMPLES
            node.add_child(child)
            if is_random:
                for i in range(RANDOM_MOVE_SAMPLES - 1):
                    child = Node(deepcopy(node.game))
                    child.state = action
                    try:
                        playTurnSparse(child.game, action)
                    except GameOver:
                        child.finished = True
                    child.player_number = child.game.current_player.entity_id - 1
                    child.policy_value = expert_policy_values[0, action] / RANDOM_MOVE_SAMPLES
                    node.add_child(child)
    if node.parent is not None:
        if node.original_player != node.player_number:
            win_value *= -1
        node.update_win_value(float(win_value), simulatingPlayer)
