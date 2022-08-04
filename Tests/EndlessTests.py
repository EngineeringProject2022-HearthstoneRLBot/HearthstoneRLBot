import fireplace
import numpy as np
from fireplace.exceptions import GameOver

from GameCommunication import playTurn
# from main import setup_game, mulliganRandomChoice, testGame
from fireplace.utils import *

from GameSetupUtils import mulliganRandomChoice


def networkInputTesting():
    while True:
        try:
            game = setup_game()
            mulliganRandomChoice(game)
            while True:
                print(playTurn(game, np.random.rand(252)))
        except GameOver:
            print("Game ended")


def continousTesting():
    while True:
        try:
            game = setup_game()
            mulliganRandomChoice(game)
            testGame(game)
        except GameOver:
            print("Game ended")

def testGame(game):
    try:
        while True:
            player = game.current_player
            while True:
                heropower = player.hero.power
                if heropower.is_usable() and random.random() < 0.1:
                    if heropower.requires_target():
                        heropower.use(target=random.choice(heropower.targets))
                    else:
                        heropower.use()
                    continue

                for card in player.hand:
                    if card.is_playable() and random.random() < 0.5:
                        target = None
                        if card.must_choose_one:
                            card = random.choice(card.choose_cards)
                        if card.requires_target():
                            target = random.choice(card.targets)
                        card.play(target=target)

                        if player.choice:
                            choice = random.choice(player.choice.cards)
                            player.choice.choose(choice)
                        continue
                for character in player.characters:
                    if character.can_attack():
                        character.attack(random.choice(character.targets))
                break
            game.end_turn()
    except fireplace.exceptions.InvalidAction:
        print("INVALID ACTION")
