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


def _setup_game(gameData):
    # we setup our game here
    from fireplace.game import Game
    from fireplace.player import Player

    randomClassOne = random.randrange(2, 10)
    randomClassTwo = random.randrange(2, 10)
    deck1 = random_draft(CardClass(randomClassOne))
    deck2 = random_draft(CardClass(randomClassTwo))
    gameData.append((randomClassOne, deck1, randomClassTwo, deck2))
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
        #gamedata 1 <-> tuple(seed)
        #gamedata 2 <-> tuple(class1, deck1, class2, deck2)
        #gamedata 3 <-> n tuple(input,probabilities,player,movement)
        #gamedata n

        # generowanie seeda (z neta) aby był losowy oraz dało się go zapisać
        gameSeed = random.randrange(sys.maxsize)
        rng = random.Random(gameSeed)

        random.seed(gameSeed)
        gameData = []
        gameData.append((gameSeed))
        game = _setup_game(gameData)
        montecarlo = MonteCarlo(Node(game), model)
        montecarlo.child_finder = child_finder
        # if doPrints:
        print("game " + str(i))
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
                print("Turn: " + str(montecarlo.root_node.parent.game.turn))
                gameData.append(((currInput[:, :, :, 0:3], currInput[0, 0, 0, 3]), probabilities, currPlayer,
                                 montecarlo.root_node.state))
                playTurnSparse(montecarlo.root_node.parent.game, montecarlo.root_node.state)
                print(montecarlo.root_node.state)

                # if len(game.moves) >= 120:  # game too long, auto-draw
                #     break
        except GameOver as e:
            if montecarlo.root_node.game.player1.playstate is PlayState.WON:
                winner = 1
                print("Game end")
            elif montecarlo.root_node.game.player2.playstate is PlayState.WON:
                winner = 2
                print("Game End")
            else:
                winner = 3
                print("Unknown")
        except Exception as e:
            winner = 4
            gameData.append((e.format_exc()))
            print(e.format_exc())
        totalData.append((gameData, winner))
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
        try:
            is_random = playTurnSparse(child.game, action)
        except GameOver:
            win_value = 1
            child.finished = True
        #if is_random:
        #   pass
        child.player_number = child.game.current_player.entity_id - 1
        child.policy_value = expert_policy_values[0, action]
        node.add_child(child)
    if node.parent is not None:
        if node.original_player != node.player_number:
            win_value *= -1
        node.update_win_value(float(win_value), simulatingPlayer)
