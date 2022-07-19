import pickle
from random import random

from fireplace.exceptions import GameOver
from fireplace.utils import random_draft
from hearthstone.enums import CardClass, PlayState

from montecarlo.montecarlo import MonteCarlo
from montecarlo.node import Node


def setup_game():
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

    return game

def selfplay(numbgame, model, simulations):
    doPrints = False  # set to True to see console
    totalData = []
    for i in range(numbgame):
        game = setup_game()
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

                # currInput = encodestate
                montecarlo.simulate(simulations, currPlayer)  # number of simulations per turn. do not put less than 2
                probabilities_value = montecarlo.get_probabilities(currPlayer)

                # probabilities = fill in probabilities for the moves, 0 for the rest

                montecarlo.root_node = montecarlo.make_exploratory_choice(currPlayer)
                # else:
                #    montecarlo.root_node = montecarlo.make_choice(currPlayer) #rest of moves are the network playing "optimally"

                if montecarlo.root_node.visits[montecarlo.root_node.original_player - 1] != 0:
                    montecarlo.root_node.visits[montecarlo.root_node.original_player - 1] -= 1

                game.move(montecarlo.root_node.state.moves[-1])
                #gameData.append((currInput, probabilities, 0, currPlayer))

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


def child_finder(node, self):
    pass
