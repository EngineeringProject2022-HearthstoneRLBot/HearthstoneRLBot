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


def _new_setup_game(data):
    from fireplace.game import Game
    from fireplace.player import Player
    BasicDruid = [2, 'EX1_169', 'EX1_169', 'CS2_005', 'CS2_005', 'CS2_189', 'CS2_189', 'CS2_120', 'CS2_120', 'CS2_009',
                  'CS2_009', 'CS2_013', 'CS2_013', 'CS2_007', 'CS2_007', 'CS2_127', 'CS2_127', 'CS2_182', 'CS2_182',
                  'CS2_119', 'CS2_119', 'DS1_055', 'DS1_055', 'EX1_593', 'EX1_593', 'CS2_200', 'CS2_200', 'CS2_162',
                  'CS2_162', 'CS2_201', 'CS2_201']
    BasicHunter = [3, 'DS1_185', 'DS1_185', 'CS2_171', 'CS2_171', 'DS1_175', 'DS1_175', 'DS1_184', 'DS1_184', 'CS2_172',
                   'CS2_172', 'CS2_120', 'CS2_120', 'CS2_141', 'CS2_141', 'CS2_122', 'CS2_122', 'CS2_196', 'CS2_196',
                   'CS2_127', 'CS2_127', 'DS1_070', 'DS1_070', 'DS1_183', 'DS1_183', 'CS2_119', 'CS2_119', 'CS2_150',
                   'CS2_150', 'CS2_201', 'CS2_201']
    BasicMage = [4, 'CFM_623', 'CFM_623', 'CS2_168', 'CS2_168', 'CS2_025', 'CS2_025', 'CS2_172', 'CS2_172', 'EX1_050',
                 'EX1_050', 'CS2_120', 'CS2_120', 'CS2_023', 'CS2_023', 'CS2_122', 'CS2_122', 'CS2_124', 'CS2_124',
                 'CS2_029', 'CS2_029', 'CS2_119', 'CS2_119', 'CS2_022', 'CS2_022', 'CS2_179', 'CS2_179', 'EX1_593',
                 'EX1_593', 'CS2_200', 'CS2_200']
    BasicPaladin = [5, 'CS2_087', 'CS2_087', 'CS1_042', 'CS1_042', 'EX1_371', 'EX1_371', 'CS2_091', 'CS2_091',
                    'CS2_171',
                    'CS2_171', 'CS2_089', 'CS2_089', 'CS2_141', 'CS2_141', 'CS2_122', 'CS2_122', 'CS2_147', 'CS2_147',
                    'CS2_094', 'CS2_094', 'CS2_131', 'CS2_131', 'EX1_593', 'EX1_593', 'CS2_150', 'CS2_150', 'CS2_162',
                    'CS2_162', 'CS2_222', 'CS2_222']
    BasicPriest = [6, 'CS2_189', 'CS2_189', 'CS1_130', 'CS1_130', 'CS2_235', 'CS2_235', 'CS2_004', 'CS2_004', 'EX1_011',
                   'EX1_011', 'EX1_192', 'EX1_192', 'CS2_172', 'CS2_172', 'CS2_121', 'CS2_121', 'CS2_234', 'CS2_234',
                   'EX1_019', 'EX1_019', 'CS2_127', 'CS2_127', 'CS2_182', 'CS2_182', 'CS2_179', 'CS2_179', 'EX1_399',
                   'EX1_399', 'CS2_201', 'CS2_201']
    BasicRogue = [7, 'CS2_072', 'CS2_072', 'CS2_074', 'CS2_074', 'CS2_189', 'CS2_189', 'CS1_042', 'CS1_042', 'CS2_075',
                  'CS2_075', 'CS2_172', 'CS2_172', 'EX1_050', 'EX1_050', 'EX1_581', 'EX1_581', 'CS2_141', 'CS2_141',
                  'EX1_025', 'EX1_025', 'CS2_147', 'CS2_147', 'CS2_131', 'CS2_131', 'CS2_076', 'CS2_076', 'EX1_593',
                  'EX1_593', 'CS2_150', 'CS2_150']
    BasicShaman = [8, 'CS2_041', 'CS2_041', 'CS2_037', 'CS2_037', 'CS2_171', 'CS2_171', 'CS2_121', 'CS2_121', 'CS2_045',
                   'CS2_045', 'CS2_039', 'CS2_039', 'CS2_122', 'CS2_122', 'CS2_124', 'CS2_124', 'CS2_182', 'CS2_182',
                   'EX1_246', 'EX1_246', 'CS2_179', 'CS2_179', 'CS2_187', 'CS2_187', 'CS2_226', 'CS2_226', 'CS2_200',
                   'CS2_200', 'CS2_213', 'CS2_213']
    BasicWarlock = [9, 'CS2_168', 'CS2_168', 'CS2_065', 'CS2_065', 'EX1_011', 'EX1_011', 'CS2_142', 'CS2_142',
                    'CS2_120',
                    'CS2_120', 'EX1_306', 'EX1_306', 'CS2_061', 'CS2_061', 'CS2_057', 'CS2_057', 'CS2_124', 'CS2_124',
                    'CS2_182', 'CS2_182', 'CS2_062', 'CS2_062', 'CS2_197', 'CS2_197', 'DS1_055', 'DS1_055', 'CS2_213',
                    'CS2_213', 'CS2_186', 'CS2_186']
    BasicWarrior = [10, 'CS2_168', 'CS2_168', 'CS2_108', 'CS2_108', 'CS2_121', 'CS2_121', 'CS2_105', 'CS2_105',
                    'EX1_506',
                    'EX1_506', 'CS2_106', 'CS2_106', 'CS2_196', 'CS2_196', 'CS2_103', 'CS2_103', 'EX1_084', 'EX1_084',
                    'CS2_124', 'CS2_124', 'EX1_025', 'EX1_025', 'CS2_179', 'CS2_179', 'EX1_399', 'EX1_399', 'CS2_200',
                    'CS2_200', 'CS2_162', 'CS2_162']

    MidrangeDruid = [2, 'EX1_169', 'EX1_169', 'AT_037', 'AT_037', 'AT_038', 'EX1_154', 'EX1_154', 'CS2_011', 'CS2_011',
                     'CS2_013', 'CS2_013', 'EX1_166', 'EX1_166', 'AT_039', 'AT_039', 'EX1_165', 'EX1_165', 'EX1_571',
                     'EX1_571', 'NEW1_008', 'NEW1_008', 'EX1_005', 'GVG_096', 'GVG_096', 'EX1_284', 'FP1_030',
                     'BRM_028',
                     'GVG_110', 'CS2_012', 'CS2_012']
    AggroHunter = [3, 'LOOT_222', 'LOOT_222', 'LOOT_258', 'LOOT_258', 'UNG_912', 'UNG_912', 'EX1_066', 'UNG_915',
                   'UNG_915',
                   'LOOT_413', 'LOOT_413', 'NEW1_031', 'NEW1_031', 'ICC_419', 'ICC_419', 'EX1_539', 'EX1_539',
                   'EX1_538',
                   'GIL_828', 'GIL_828', 'LOOT_077', 'DS1_070', 'DS1_070', 'GIL_650', 'EX1_048', 'EX1_048', 'DS1_178',
                   'EX1_531', 'EX1_534', 'EX1_534']
    MechMage = [4, 'NEW1_012', 'CS2_024', 'CS2_024', 'GVG_002', 'GVG_002', 'GVG_003', 'CS2_029', 'CS2_029', 'GVG_004',
                'GVG_004', 'CS2_033', 'CS2_033', 'EX1_559', 'GVG_082', 'GVG_082', 'GVG_013', 'GVG_013', 'GVG_085',
                'GVG_085', 'GVG_006', 'GVG_006', 'GVG_044', 'GVG_044', 'GVG_102', 'GVG_078', 'FP1_030', 'GVG_115',
                'GVG_110', 'GVG_096', 'GVG_096']
    ControlPaladin = [5, 'EX1_360', 'EX1_619', 'EX1_619', 'CS2_089', 'EX1_382', 'EX1_382', 'CS2_093', 'CS2_093',
                      'LOE_017',
                      'LOE_017', 'CS2_097', 'CS2_097', 'AT_104', 'EX1_354', 'EX1_383', 'NEW1_020', 'NEW1_020',
                      'EX1_007',
                      'EX1_007', 'EX1_085', 'EX1_005', 'CS2_179', 'CS2_179', 'EX1_048', 'EX1_564', 'NEW1_041',
                      'EX1_032',
                      'EX1_016', 'EX1_298', 'EX1_572']
    ControlPriest = [6, 'EX1_621', 'EX1_621', 'GVG_012', 'GVG_012', 'CS2_235', 'CS2_235', 'CS2_004', 'CS2_004',
                     'FP1_001',
                     'FP1_001', 'EX1_622', 'EX1_622', 'EX1_339', 'EX1_339', 'NEW1_020', 'NEW1_020', 'FP1_009',
                     'CS2_181',
                     'CS2_181', 'EX1_591', 'EX1_591', 'CS1_112', 'FP1_012', 'FP1_012', 'CS2_186', 'EX1_091', 'AT_132',
                     'GVG_008', 'GVG_008', 'EX1_572']
    OilRogue = [7, 'CS2_072', 'CS2_072', 'EX1_145', 'EX1_145', 'CS2_074', 'CS2_074', 'CS2_233', 'CS2_233', 'EX1_124',
                'EX1_124', 'EX1_581', 'EX1_581', 'EX1_613', 'EX1_129', 'EX1_129', 'EX1_134', 'EX1_134', 'GVG_022',
                'GVG_022', 'CS2_077', 'CS2_077', 'EX1_012', 'CS2_117', 'CS2_117', 'GVG_096', 'NEW1_026', 'NEW1_026',
                'EX1_284', 'EX1_284', 'FP1_030']
    MidrangeShaman = [8, 'EX1_245', 'GVG_038', 'GVG_038', 'EX1_565', 'EX1_565', 'CS2_045', 'CS2_045', 'EX1_248',
                      'EX1_248',
                      'EX1_259', 'EX1_259', 'EX1_575', 'EX1_246', 'EX1_246', 'EX1_567', 'CS2_042', 'CS2_042',
                      'NEW1_010',
                      'EX1_012', 'FP1_002', 'FP1_002', 'EX1_093', 'EX1_093', 'GVG_096', 'GVG_096', 'GVG_069', 'EX1_284',
                      'EX1_284', 'FP1_030', 'GVG_110']
    DemonZoo = [9, 'EX1_319', 'EX1_319', 'EX1_316', 'EX1_316', 'CS2_065', 'CS2_065', 'LOE_023', 'LOE_023', 'BRM_006',
                'BRM_006', 'EX1_304', 'GVG_045', 'GVG_045', 'FP1_022', 'FP1_022', 'EX1_310', 'EX1_310', 'GVG_021',
                'CS2_188', 'CS2_188', 'FP1_002', 'FP1_002', 'NEW1_019', 'NEW1_019', 'FP1_007', 'FP1_007', 'CS2_203',
                'EX1_093', 'EX1_093', 'GVG_110']
    MidrangeWarrior = [10, 'CS2_108', 'CS2_108', 'EX1_410', 'EX1_410', 'EX1_402', 'EX1_402', 'EX1_603', 'EX1_603',
                       'BRM_015',
                       'CS2_106', 'CS2_106', 'EX1_606', 'EX1_606', 'FP1_021', 'FP1_021', 'EX1_407', 'GVG_053',
                       'GVG_053',
                       'EX1_414', 'EX1_007', 'EX1_007', 'EX1_005', 'EX1_558', 'FP1_012', 'FP1_012', 'EX1_016',
                       'EX1_249',
                       'GVG_110', 'EX1_561', 'EX1_572']

    FastDruid = [2, 'EX1_169', 'EX1_169', 'EX1_154', 'EX1_154', 'CS2_011', 'CS2_011', 'CS2_013', 'CS2_013', 'EX1_166',
                 'EX1_166', 'CS2_012', 'CS2_012', 'EX1_165', 'EX1_165', 'EX1_571', 'NEW1_008', 'NEW1_008', 'EX1_573',
                 'FP1_001', 'EX1_085', 'FP1_005', 'FP1_005', 'EX1_005', 'GVG_096', 'GVG_096', 'EX1_284', 'EX1_558',
                 'FP1_012', 'EX1_016', 'GVG_110']
    FaceHunter = [3, 'GVG_043', 'GVG_043', 'BRM_013', 'BRM_013', 'NEW1_031', 'NEW1_031', 'EX1_536', 'EX1_536',
                  'EX1_539',
                  'EX1_539', 'EX1_538', 'EX1_538', 'CS2_188', 'CS2_188', 'EX1_008', 'EX1_008', 'EX1_029', 'EX1_029',
                  'FP1_002', 'FP1_002', 'NEW1_019', 'NEW1_019', 'AT_084', 'AT_084', 'EX1_089', 'EX1_089', 'AT_087',
                  'AT_087', 'CS2_203', 'CS2_203']
    FlamewalkerTempoMage = [4, 'EX1_277', 'EX1_277', 'NEW1_012', 'NEW1_012', 'GVG_001', 'GVG_001', 'CS2_024', 'CS2_024',
                            'GVG_003', 'GVG_003', 'BRM_002', 'BRM_002', 'CS2_029', 'CS2_029', 'EX1_608', 'EX1_608',
                            'CS2_032', 'CS2_032', 'EX1_066', 'EX1_066', 'GVG_096', 'GVG_096', 'EX1_284', 'EX1_284',
                            'FP1_012', 'FP1_012', 'FP1_030', 'EX1_016', 'GVG_110', 'EX1_298']
    MurlocPaladin = [5, 'GVG_058', 'GVG_058', 'EX1_382', 'EX1_382', 'GVG_059', 'GVG_061', 'GVG_061', 'CS2_093',
                     'CS2_093',
                     'LOE_017', 'CS2_097', 'BRM_001', 'EX1_354', 'LOE_026', 'FP1_001', 'CS2_173', 'CS2_173', 'NEW1_019',
                     'EX1_096', 'EX1_096', 'EX1_507', 'EX1_507', 'EX1_595', 'EX1_062', 'GVG_096', 'GVG_096', 'GVG_069',
                     'GVG_069', 'FP1_012', 'GVG_110']
    DragonPriest = [6, 'CS2_235', 'CS2_235', 'CS2_004', 'CS2_004', 'BRM_004', 'BRM_004', 'EX1_622', 'EX1_622',
                    'CS2_234',
                    'AT_116', 'AT_116', 'FP1_023', 'GVG_010', 'GVG_010', 'CS1_112', 'CS1_112', 'CS2_186', 'NEW1_020',
                    'BRM_033', 'BRM_033', 'BRM_020', 'AT_017', 'AT_017', 'EX1_284', 'EX1_284', 'BRM_034', 'BRM_034',
                    'AT_123', 'BRM_031', 'EX1_572']
    AllDecks = [BasicDruid, BasicHunter, BasicMage, BasicPaladin, BasicPriest, BasicRogue, BasicShaman, BasicWarlock,
                BasicWarrior,
                MidrangeDruid, AggroHunter, MechMage, ControlPaladin, ControlPriest, OilRogue, MidrangeShaman, DemonZoo,
                MidrangeWarrior,
                FastDruid, FaceHunter, FlamewalkerTempoMage, MurlocPaladin, DragonPriest]

    randomDeckOne = random.choice(AllDecks)
    randomDeckTwo = random.choice(AllDecks)
    classOne = randomDeckOne[0]
    classTwo = randomDeckTwo[0]
    randomDeckOne = randomDeckOne[1:len(randomDeckOne)]
    randomDeckTwo = randomDeckTwo[1:len(randomDeckTwo)]

    deck1 = randomDeckOne
    deck2 = randomDeckTwo
    if data is not None:
        data.append((classOne, deck1, classTwo, deck2))
    player1 = Player("Player1", deck1, CardClass(classOne).default_hero)
    player2 = Player("Player2", deck2, CardClass(classTwo).default_hero)

    game = Game(players=(player1, player2))
    game.start()
    mulliganRandomChoice(game)
    return game


def _setup_game(data):
    # we setup our game here
    from fireplace.game import Game
    from fireplace.player import Player

    randomClassOne = random.randrange(2, 10)
    randomClassTwo = random.randrange(2, 10)
    # deck1 = random_draft(CardClass(randomClassOne))
    # deck2 = random_draft(CardClass(randomClassTwo))
    deck1 = ['EX1_169', 'EX1_169', 'EX1_154', 'EX1_154', 'CS2_011', 'CS2_011', 'CS2_013', 'CS2_013', 'EX1_166',
             'EX1_166', 'CS2_012', 'CS2_012', 'EX1_165', 'EX1_165', 'EX1_571', 'NEW1_008', 'NEW1_008', 'EX1_573',
             'FP1_001', 'EX1_085', 'FP1_005', 'FP1_005', 'EX1_005', 'GVG_096', 'GVG_096', 'EX1_284', 'EX1_558',
             'FP1_012', 'EX1_016', 'GVG_110']
    deck2 = ['GVG_043', 'GVG_043', 'BRM_013', 'BRM_013', 'NEW1_031', 'NEW1_031', 'EX1_536', 'EX1_536', 'EX1_539',
             'EX1_539', 'EX1_538', 'EX1_538', 'CS2_188', 'CS2_188', 'EX1_008', 'EX1_008', 'EX1_029', 'EX1_029',
             'FP1_002', 'FP1_002', 'NEW1_019', 'NEW1_019', 'AT_084', 'AT_084', 'EX1_089', 'EX1_089', 'AT_087', 'AT_087',
             'CS2_203', 'CS2_203']
    if data is not None:
        data.append((randomClassOne, deck1, randomClassTwo, deck2))
    player1 = Player("Player1", deck1, CardClass(randomClassOne).default_hero)
    player2 = Player("Player2", deck2, CardClass(randomClassTwo).default_hero)

    game = Game(players=(player1, player2))
    game.start()
    mulliganRandomChoice(game)
    return game

class GamePlayer():
    def __init__(self, model, simulations, seedObject=None, rand=False):
        if seedObject != None:
            random.setstate(seedObject)
        data = []
        self.game = _new_setup_game(data)
        #self.game = hunter_heropower_test()
        self.data = []
        # game = mage_heropower_test()
        if not rand:
            self.model = model
            self.simulations = simulations
            self.montecarlo = []
            for i in range(2):
                tmp = MonteCarlo(Node(self.game), self.model)
                tmp.child_finder = child_finder
                tmp.root_node.player_number = 1 if self.game.current_player is self.game.player1 else 2
                tmp.player_number = 1 if self.game.current_player is self.game.player1 else 2
                self.montecarlo.append(tmp)


    def playRandGame(self):
        try:
            while True:
                #game.current_player.discard_hand()
                currPlayer = 1 if self.game.current_player is self.game.player1 else 2
                currInput = InputBuilder.convToInput(self.game)
                actions = checkValidActionsSparse(self.game)
                action = random.choice(actions)
                probabilities = np.zeros(252)
                for poss_action in actions:
                    probabilities[poss_action] = 1 / len(actions)
                    # probably unnecessary: add the tiny difference to ensure probabilities add to 1
                    if poss_action == actions[-1]:
                        probabilities[poss_action] += 1 - sum(probabilities)
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
                print("Turn: " + str(self.game.turn) + ", Action:" + str(action) + " - ",
                      (interpretDecodedAction(decodeAction(action), self.game)))
                self.data.append((currInput, probabilities, currPlayer, action))
                # to wywolanie bedzie wrapperowane w jakas funkcje playturn czy cos podobnego
                play_rand_turn(self.game, action)



        except GameOver as e:
            currPlayer = 1 if self.game.current_player is self.game.player1 else 2
            currInput = InputBuilder.convToInput(self.game)
            self.data.append((currInput, np.zeros(252), currPlayer, None))

            if self.game.current_player.playstate is PlayState.WON:
                winner = currPlayer
            elif self.game.current_player.opponent.playstate is PlayState.WON:
                winner = 2 if currPlayer == 1 else 1
            else:
                winner = 3
        except NoChildException as e:
            winner = 4
            self.data.append(traceback.format_exc())
            print(traceback.format_exc())
            # handle this issue, record it into the data
        except Exception as e:
            winner = 4
            self.data.append(traceback.format_exc())
            print(traceback.format_exc())
        return winner, self.data


    def playGame(self):
        # montecarlo = MonteCarlo(Node(game), model)
        # montecarlo.child_finder = child_finder
        # montecarlo.root_node.player_number = game.current_player.entity_id - 1
        winner = 0

        try:
            while True:
                #self.game.current_player.discard_hand()


                currPlayer = 1 if self.game.current_player is self.game.player1 else 2
                (currTree, otherTree) = (self.montecarlo[0], self.montecarlo[1]) if currPlayer == 1 else (
                    self.montecarlo[1], self.montecarlo[0])
                currInput = InputBuilder.convToInput(currTree.root_node.game)
                currTree.simulate(self.simulations)  # number of simulations per turn. do not put less than 2

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
                print("Turn: " + str(self.game.turn) + ", Action:" + str(action) + " - ",
                      (interpretDecodedAction(decodeAction(action), self.game)))
                self.data.append((currInput, probabilities, currPlayer, action))
                # to wywolanie bedzie wrapperowane w jakas funkcje playturn czy cos podobnego
                play_monte_carlo_turn(self.game, action, trees=self.montecarlo)



        except GameOver as e:
            currPlayer = 1 if self.game.current_player is self.game.player1 else 2
            currInput = InputBuilder.convToInput(self.game)
            self.data.append((currInput, np.zeros(252), currPlayer, None))

            if self.game.current_player.playstate is PlayState.WON:
                winner = currPlayer
            elif self.game.current_player.opponent.playstate is PlayState.WON:
                winner = 2 if currPlayer == 1 else 1
            else:
                winner = 3
        except NoChildException as e:
            winner = 4
            self.data.append(traceback.format_exc())
            print(traceback.format_exc())
            # handle this issue, record it into the data
        except Exception as e:
            winner = 4
            self.data.append(traceback.format_exc())
            print(traceback.format_exc())
        return winner, self.data


def play_rand_turn(game, action=None):
    if action is None:
        actions = checkValidActionsSparse(game)
        action = random.choice(actions)
    is_random = playTurnSparse(game, action)


def play_monte_carlo_turn(game, action=None, currTree=None, simulations=50, trees=None):
    if trees is None:
        trees = []
    if action is None:
        currTree.simulate(simulations)  # number of simulations per turn. do not put less than 2
        action = currTree.make_exploratory_choice().state
    is_random = playTurnSparse(game, action)
    for x in trees:
        x.sync_tree(game, action, is_random)
        x.root_node.parent = None


def child_finder(node, montecarlo):
    #node.game.current_player.discard_hand()
    if node.game.current_player.hero.health == 0 and node.game.current_player.opponent.hero.health == 1:
        a = "a"
    # if we have 50 simulations, and after doing 35 we have reached an end node, we are going to "explore this node 15
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
            child.stateText = ("Action:" + str(action) + " - " + interpretDecodedAction(decodeAction(action), node.game))
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
