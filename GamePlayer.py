import traceback
from copy import deepcopy
import random

from fireplace.exceptions import GameOver
from fireplace.utils import random_draft
from hearthstone.enums import CardClass, PlayState

from GameCommunication import checkValidActionsSparse, playTurnSparse
from GameSetupUtils import mulliganRandomChoice
from GameState import InputBuilder
from Tests.ScenarioTests import weapon_test
from montecarlo.montecarlo import MonteCarlo
from montecarlo.node import Node, NoChildException

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


def playGame(model, simulations, seedObject=None):
    if seedObject != None:
        random.setstate(seedObject)
    data = []
    game = _setup_game(data)
    # game = weapon_test()
    montecarlo = []
    for i in range(2):
        tmp = MonteCarlo(Node(game), model)
        tmp.child_finder = child_finder
        tmp.root_node.player_number = 1 if game.current_player is game.player1 else 2
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
            currInput = InputBuilder.convToInput(currTree.root_node.game, currPlayer)
            currTree.simulate(simulations)  # number of simulations per turn. do not put less than 2


            probabilities = currTree.get_probabilities()

            action = currTree.make_exploratory_choice().state

            # else:
            #    montecarlo.root_node = montecarlo.make_choice(currPlayer)
            #    #rest of moves are the network playing "optimally"

            # zamieniłem bo chcemy appendować co zrobiliśmy i dopiero wtedy zagrać turę - ten ostatni ruch
            # spowodował naszą wygraną (co nie byłoby zapisane do pliku, bo exception)
            print("Turn: " + str(game.turn) + ", Action:" + str(action))

            data.append((currInput, probabilities, currPlayer, action))
            # to wywolanie bedzie wrapperowane w jakas funkcje playturn czy cos podobnego
            is_random = playTurnSparse(game, action)

            for x in montecarlo:
                x.sync_tree(game, action, is_random)
                x.root_node.parent = None

            # if len(game.moves) >= 120:  # game too long, auto-draw
            #     break
    except GameOver as e:
        if game.player1.playstate is PlayState.WON:
            winner = 1
        elif game.player2.playstate is PlayState.WON:
            winner = 2
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
        node.update_win_value(float(win_value))
