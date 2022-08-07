import pickle
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


def _setup_game():
    # we setup our game here
    from fireplace.game import Game
    from fireplace.player import Player

    randomClassOne = random.randrange(2, 10)
    randomClassTwo = random.randrange(2, 10)
    deck1 = random_draft(CardClass(randomClassOne))
    deck2 = random_draft(CardClass(randomClassTwo))
    player1 = Player("Player1", deck1, CardClass(randomClassOne).default_hero)
    player2 = Player("Player2", deck2, CardClass(randomClassTwo).default_hero)

    game = Game(players=(player1, player2))
    game.start()
    mulliganRandomChoice(game)
    return game

def selfplay(numbgame, model, simulations):
    doPrints = False  # set to True to see console
    totalData = []
    for i in range(numbgame):
        game = _setup_game()
        montecarlo = MonteCarlo(Node(game), model)
        gameData = []
        montecarlo.child_finder = child_finder
        # if doPrints:
        print("game " + str(i))
        montecarlo.root_node.player_number = 1
        winner = 0
        while True:
            # game state
            try:
                currPlayer = game.current_player.entity_id - 1

                currInput = InputBuilder.convToInput(game, currPlayer)
                montecarlo.simulate(simulations, currPlayer)  # number of simulations per turn. do not put less than 2
                probabilities = montecarlo.get_probabilities(currPlayer)

                montecarlo.root_node = montecarlo.make_exploratory_choice(currPlayer)
                # else:
                #    montecarlo.root_node = montecarlo.make_choice(currPlayer) #rest of moves are the network playing "optimally"

                if montecarlo.root_node.visits[montecarlo.root_node.original_player - 1] != 0:
                    montecarlo.root_node.visits[montecarlo.root_node.original_player - 1] -= 1

                playTurnSparse(montecarlo.root_node.parent.game, montecarlo.root_node.state)
                gameData.append((currInput, probabilities, currPlayer))

                # if len(game.moves) >= 120:  # game too long, auto-draw
                #     break
            except GameOver:
                if game.player1.playstate is PlayState.WON:
                    winner = 1
                elif game.player2.playstate is PlayState.WON:
                    winner = 2
                break
        for state in gameData:
            data = list(state)
            if data[2] == winner:
                data[2] = 1
            elif winner is not None:
                data[2] = -1
            else:
                data[2] = 0  # already equal to zero but done for clarity
            totalData.append((data[0], data[1], data[2]))
        with open("TrainingData.txt", "wb") as fp:
            pickle.dump(totalData, fp)
    return totalData


def child_finder(node, montecarlo, simulatingPlayer):

    node.original_player = simulatingPlayer
    x = InputBuilder.convToInput(node.game, node.player_number)

    expert_policy_values, win_value = montecarlo.model(x)
    for action in checkValidActionsSparse(node.game):
        child = Node(deepcopy(node.game))
        child.state = action
        playTurnSparse(child.game, action)
        child.player_number = child.game.current_player.entity_id - 1
        child.policy_value = expert_policy_values[0, action]
        node.add_child(child)
    if node.parent is not None:
        if node.original_player != node.player_number:
            win_value *= -1
        node.update_win_value(float(win_value), simulatingPlayer)
