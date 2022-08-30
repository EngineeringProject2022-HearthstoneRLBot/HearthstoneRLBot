import traceback
from copy import deepcopy
import random

import numpy as np
from fireplace.exceptions import GameOver
from fireplace.utils import random_draft
from hearthstone.enums import CardClass, PlayState

from GameCommunication import checkValidActionsSparse, playTurnSparse
from GameSetupUtils import mulliganRandomChoice
from GameState import InputBuilder
from Tests.ScenarioTests import weapon_test, simpler_weapon_test, mage_heropower_test, hunter_heropower_test
from montecarlo.montecarlo import MonteCarlo
from montecarlo.node import Node, NoChildException

from GameConvenience import getCardIdFromAction, interpretDecodedAction, decodeAction

RANDOM_MOVE_SAMPLES = 5


def _setup_game(data):
    # we setup our game here
    from fireplace.game import Game
    from fireplace.player import Player

    randomClassOne = random.randrange(2, 10)
    randomClassTwo = random.randrange(2, 10)
    #deck1 = random_draft(CardClass(randomClassOne))
    #deck2 = random_draft(CardClass(randomClassTwo))
    deck1 = ['EX1_169', 'EX1_169', 'EX1_154', 'EX1_154', 'CS2_011', 'CS2_011', 'CS2_013', 'CS2_013', 'EX1_166', 'EX1_166', 'CS2_012', 'CS2_012', 'EX1_165', 'EX1_165', 'EX1_571', 'NEW1_008', 'NEW1_008', 'EX1_573', 'FP1_001', 'EX1_085', 'FP1_005', 'FP1_005', 'EX1_005', 'GVG_096', 'GVG_096', 'EX1_284', 'EX1_558', 'FP1_012', 'EX1_016', 'GVG_110']
    deck2 = ['GVG_043', 'GVG_043', 'BRM_013', 'BRM_013', 'NEW1_031', 'NEW1_031', 'EX1_536', 'EX1_536', 'EX1_539', 'EX1_539', 'EX1_538', 'EX1_538', 'CS2_188', 'CS2_188', 'EX1_008', 'EX1_008', 'EX1_029', 'EX1_029', 'FP1_002', 'FP1_002', 'NEW1_019', 'NEW1_019', 'AT_084', 'AT_084', 'EX1_089', 'EX1_089', 'AT_087', 'AT_087', 'CS2_203', 'CS2_203']
    data.append((randomClassOne, deck1, randomClassTwo, deck2))
    player1 = Player("Player1", deck1, CardClass(randomClassOne).default_hero)
    player2 = Player("Player2", deck2, CardClass(randomClassTwo).default_hero)

    game = Game(players=(player1, player2))
    game.start()
    mulliganRandomChoice(game)
    return game


def playGame(model, simulations, seedObject=None):
    if seedObject != None:
        random.setstate(seedObject)
    data = []
    cardsp1 = []
    cardsp2 = []
    game = _setup_game(data)
    #game = hunter_heropower_test()
    montecarlo = []
    for i in range(2):
        tmp = MonteCarlo(Node(game), model)
        tmp.child_finder = child_finder
        tmp.root_node.player_number = 1 if game.current_player is game.player1 else 2
        tmp.player_number = i + 1
        montecarlo.append(tmp)
    # montecarlo = MonteCarlo(Node(game), model)
    # montecarlo.child_finder = child_finder
    # montecarlo.root_node.player_number = game.current_player.entity_id - 1
    winner = 0

    try:
        while True:
            currPlayer = 1 if game.current_player is game.player1 else 2
            (currTree, otherTree) = (montecarlo[0], montecarlo[1]) if currPlayer == 1 else (
                montecarlo[1], montecarlo[0])
            currInput = InputBuilder.convToInput(currTree.root_node.game)
            currTree.simulate(simulations)  # number of simulations per turn. do not put less than 2


            probabilities = currTree.get_probabilities()

            action = currTree.make_exploratory_choice().state
            # This part will collect the order in which players played their cards
            # For now commented as it raises some errors in some cases
            # if game.current_player is game.player1:
            #     card = getCardIdFromAction(action, game)
            #     if card is not None:
            #         cardsp1.append(card)
            # elif game.current_player is game.player2:
            #     card = getCardIdFromAction(action, game)
            #     if card is not None:
            #         cardsp2.append(card)

            # else:
            #    montecarlo.root_node = montecarlo.make_choice(currPlayer)
            #    #rest of moves are the network playing "optimally"

            # zamieniłem bo chcemy appendować co zrobiliśmy i dopiero wtedy zagrać turę - ten ostatni ruch
            # spowodował naszą wygraną (co nie byłoby zapisane do pliku, bo exception)
            print("Turn: " + str(game.turn) + ", Action:" + str(action) + " - ", (interpretDecodedAction(decodeAction(action), game)))
            data.append((currInput, probabilities, currPlayer, action))
            # to wywolanie bedzie wrapperowane w jakas funkcje playturn czy cos podobnego
            is_random = playTurnSparse(game, action)

            for x in montecarlo:
                x.sync_tree(game, action, is_random)
                x.root_node.parent = None

    except GameOver as e:
        currPlayer = 1 if game.current_player is game.player1 else 2
        currInput = InputBuilder.convToInput(game)
        data.append((currInput, np.zeros(252), currPlayer, None))

        if game.current_player.playstate is PlayState.WON:
            winner = currPlayer
        elif game.current_player.opponent.playstate is PlayState.WON:
            winner = 2 if currPlayer == 1 else 1
        else:
            winner = 3
    except NoChildException as e:
        winner = 4
        data.append(traceback.format_exc())
        print(traceback.format_exc())
        # handle this issue, record it into the data
    except Exception as e:
        winner = 4
        data.append(traceback.format_exc())
        print(traceback.format_exc())
    return winner, data


def child_finder(node, montecarlo):
    if node.game.current_player.hero.health == 0 and node.game.current_player.opponent.hero.health == 1:
        a = "a"
    #if we have 50 simulations, and after doing 35 we have reached an end node, we are going to "explore this node 15
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
            is_random = 0
            try:
                is_random = playTurnSparse(child.game, action)
            except GameOver:
                child.finished = True
            child.player_number = 1 if child.game.current_player is child.game.player1 else 2
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
                    child.player_number = 1 if child.game.current_player is child.game.player1 else 2
                    child.policy_value = expert_policy_values[0, action] / RANDOM_MOVE_SAMPLES
                    node.add_child(child)
    if node.parent is not None:
        node.update_win_value(float(win_value))
