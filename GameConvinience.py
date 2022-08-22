import fireplace
from hearthstone.enums import CardClass
from fireplace import cards, logging

# import os
# os.environ['PYTHONHASHSEED'] = '0' # niby mi działa z zakomentowanymi tymi liniami, ale zostawiam na później
# os.environ['CUDA_VISIBLE_DEVICES'] = '' #czy to nie zepsuje procesowania z CUDA?
from GameCommunication import checkValidActionsSparse, playTurnSparse
from GameSetupUtils import prepare_game
from GameState import Hero, HandCard
from fireplace.utils import *
# import os
# os.environ['PYTHONHASHSEED'] = '0' # niby mi działa z zakomentowanymi tymi liniami, ale zostawiam na później
# os.environ['CUDA_VISIBLE_DEVICES'] = '' #czy to nie zepsuje procesowania z CUDA?
import sys

def translateClassId(id):
    if id == 2:
        idstr = 'Druid'
    elif id == 3:
        idstr = 'Hunter'
    elif id == 4:
        idstr = 'Mage'
    elif id == 5:
        idstr = 'Paladin'
    elif id == 6:
        idstr = 'Priest'
    elif id == 7:
        idstr = 'Rogue'
    elif id == 8:
        idstr = 'Shaman'
    elif id == 9:
        idstr = 'Warlock'
    elif id == 10:
        idstr = 'Warior'
    return idstr

# 0 - A1H0
# 1 - A1B1
# 2 - A1B2
# 3 - A1B3
# . . .
# 16 - A100 (zagranie bez celu)
# 17 - A2H0
# 18 - A2B1
# 19 - A2B2
#
# 17 opcji dla kazdej karty
def decodeAction(action):
    tmpAction = ''
    tmpTarget = ''
    result = ''
    if action == 251: #use end turn button
        result = 'E0000'
    elif action < 170: #use card from hand
        if action % 17 == 0:
            tmpTarget = 'H0'
        elif 1 <= action % 17 <= 7:
            tmpTarget = 'B' + str(action % 17)
        elif action % 17 == 8:
            tmpTarget = 'G0'
        elif 9 <= action % 17 < 16:
            tmpTarget = 'C' + str(action % 17 - 8)
        elif action % 17 == 16:
            tmpTarget = '00'
        tmpAction = int(action / 17) + 1
        if(tmpAction) < 10:
            result = 'A0' + str(tmpAction) + tmpTarget
        else:
            result = 'A' + str(tmpAction) + tmpTarget

    elif action < 187: #hero power usage
        if action % 17 == 0:
            tmpTarget = 'H0'
        elif 1 <= action % 17 <= 7:
            tmpTarget = 'B' + str(action % 17)
        elif action % 17 == 8:
            tmpTarget = 'G0'
        elif 9 <= action % 17 < 16:
            tmpTarget = 'C' + str(action % 17 - 8)
        elif action % 17 == 16:
            tmpTarget = '00'
        tmpAction = 0
        result = 'X0' + str(tmpAction) + tmpTarget

    else: #use a character, starting from hero
        minion = int((action-187)/8)
        miniontarget = (action-187) % 8
        if minion == 0:
            tmpTarget = 'H00'
        elif 1 <= minion <= 7:
            tmpTarget = 'B0' + str(minion)

        if miniontarget == 0:
            tmpTarget = tmpTarget + 'G0'
        elif 1 <= miniontarget <= 7:
            tmpTarget = tmpTarget + 'C' + str(miniontarget)
        result = tmpTarget
    return result

def interpretDecodedAction(result, game):
    log = ''
    src_log = ''
    target_log = ''
    tmp_player = 1 if game.current_player is game.player1 else 2

    if tmp_player == 2:
        p2 = game.player1
        p1 = game.player2
    elif tmp_player == 1:
        p1 = game.player1
        p2 = game.player2

    source_number = 0

    source = result[0]
    if result[1] == '0':
        source_number = result[2]
    elif result[1] == '1':
        source_number = result[1] + result[2]
    target = result[3]
    target_number = result[4]

    if source == 'A':
        src_log = str(p1.hero), " plays from hand card number ", source_number, " - ", p1.hand[int(source_number)-1].data.name, " -"
    elif source == 'X':
        src_log = str(p1.hero), " uses hero power - ", str(p1.hero.power), " -"
    elif source == 'H':
        src_log = str(p1.hero), " attacks"
    elif source == 'B':
        src_log = "Minion from allay board with number ", source_number, " - ", p1.field[int(source_number) - 1].data.name, " - attacks "
    elif source == 'E':
        src_log = str(p1.hero), " has ended the turn"
        src_log = ''.join(src_log)
        return src_log
    src_log = ''.join(src_log)

    if target == 'H':
        target_log = " on self"
    elif target == 'B':
        target_log = " on own minion number ", target_number, " - ", p1.field[int(target_number)-1].data.name, " -"
    elif target == 'C':
        target_log = " on enemy minion number ", target_number, " - ", p2.field[int(target_number)-1].data.name, " -"
    elif target == 'G':
        target_log = " on ", str(p2.hero)
    elif target == '0':
        target_log = ' without a target'
    target_log = ''.join(target_log)
    return(src_log + target_log)


# This function returns the card that is abot to be played based on action number and game object,
# if a card is not played (ex hero power is used instead) it returns None
def getCardIdFromAction(action, game):
    result = decodeAction(action)
    tmp_player = 1 if game.current_player is game.player1 else 2
    if tmp_player == 2:
        p2 = game.player1
        p1 = game.player2
    elif tmp_player == 1:
        p1 = game.player1
        p2 = game.player2
    source_number = 0
    source = result[0]
    if result[1] == '0':
        source_number = result[2]
    elif result[1] == '1':
        source_number = result[1] + result[2]
    if source == 'A':
        return p1.hand[int(source_number)-1].data.id
    else:
        pass

def checkPlayableHandCards(results, game):
    log = ''
    src_log = ''
    target_log = ''
    tmp_player = 1 if game.current_player is game.player1 else 2

    if tmp_player == 2:
        p2 = game.player1
        p1 = game.player2
    elif tmp_player == 1:
        p1 = game.player1
        p2 = game.player2

    source_number = []
    source = []
    target_number = []
    target = []
    for i in range(len(results)):
        #source_number = 0
        source.append(results[i][0])
        if results[i][1] == '0':
            source_number.append(results[i][2])
        elif results[i][1] == '1':
            source_number.append(results[i][1] + results[i][2])
        target.append(results[i][3])
        target_number.append(results[i][4])

    allPossibilitiesList = []
    for i in range(10):
        allPossibilitiesList.append([])

    for i in range(len(source)):
        if source[i] == 'A':
            allPossibilitiesList[int(source_number[i])-1].append((target[i], target_number[i]))
            print(allPossibilitiesList)
            print(source[i], source_number[i], target[i], target_number[i])
            #src_log = str(p1.hero), " hand card ", source_number, " - ", p1.hand[int(source_number) - 1].data.name, " -"
            #return src_log

def createHand(game):
    possible_actions_interpreted = []
    decoded_actions = []
    possible_actions = checkValidActionsSparse(game)
    for action in possible_actions:
        possible_actions_interpreted.append(interpretDecodedAction(decodeAction(action), game))
        decoded_actions.append(decodeAction(action))

    print(checkPlayableHandCards(decoded_actions, game)) #tmp for taking just possible actions for a card once

    counter = 0
    for possible_moves in possible_actions_interpreted:
        print(counter, possible_moves)
        counter += 1

    choice = input("Choose number of action: ")
    act = possible_actions[int(choice)]
    # print(getCardIdFromAction(act, game))
    playTurnSparse(game, act)
    return 0

def checkBoard(game):
    tmp_player = 1 if game.current_player is game.player1 else 2
    if tmp_player == 2:
        p2 = game.player1
        p1 = game.player2
    elif tmp_player == 1:
        p1 = game.player1
        p2 = game.player2
    for elem in p1.field:
        print("Card name:",elem.data.name, ", Cost:", elem.cost, ", Atk:", elem.atk, ", Hp:", elem.health)

# TU TYLKO MOJE TESTY, ZOSTAWIAM JE ZAKOMENTOWANE JESZCZE A POTEM JE USUNE JAK WSZYSTKO BEDZIE OGARNIETE NA 100% JKBC!!!
# for i in range(252):
#     print(decodeAction(i))
#
#
logger = logging.log
logger.disabled = True
logger.propagate = False
cards.db.initialize()
game = prepare_game()

# for elem in game.player1.deck:
#     if isinstance(elem, fireplace.card.Minion):
#         print('Minion')
#     elif isinstance(elem, fireplace.card.Spell):
#         print('Spell')
#     elif isinstance(elem, fireplace.card.Weapon):
#         print('Weapon')
#     else:
#         print("Unknown")
while True:
    print(game.player1.hero.health)
    print(game.player2.hero.health)
    checkBoard(game)
    createHand(game)

    a=0


#
# game.player1.discard_hand()
# game.player2.discard_hand()
# for i in range(1):
#     board1 = game.player1.give('CS2_231') # whisp
#     board2 = game.player1.give('GVG_093') # target dummy
#     board3 = game.player1.give('EX1_008') # argent squire
#     board4 = game.player1.give('CS2_231') # whisp
#     board5 = game.player1.give('GVG_093') # target dummy
#     board6 = game.player1.give('EX1_008') #argent squire
#     board7 = game.player1.give('CS2_231') # whisp
#     board1.play()
#     board2.play()
#     board3.play()
#     board4.play()
#     board5.play()
#     board6.play()
#     board7.play()
# game.end_turn()
# game.player1.discard_hand()
# game.player2.discard_hand()
# for i in range(1):
#     board1 = game.player2.give('CS2_231') # whisp
#     board2 = game.player2.give('GVG_093') # target dummy
#     board3 = game.player2.give('EX1_008') # argent squire
#     board4 = game.player2.give('CS2_231') # whisp
#     board5 = game.player2.give('GVG_093') # target dummy
#     board6 = game.player2.give('EX1_008') #argent squire
#     board7 = game.player2.give('CS2_231') # whisp
#     board1.play()
#     board2.play()
#     board3.play()
#     board4.play()
#     board5.play()
#     board6.play()
#     board7.play()
# game.end_turn()
# game.player1.discard_hand()
# game.player2.discard_hand()
# for i in range(1):
#     game.player1.give('EX1_169') # Claw
#     game.player1.give('EX1_277') # Arcane Missiles
#     game.player1.give('EX1_279') # Pyroblast
#     game.player1.give('EX1_284') # Azure Drake
#     game.player1.give('EX1_315') # Summoning Portal
#     game.player1.give('EX1_335') # Lightspawn
#     game.player1.give('EX1_360') # Humility
#     game.player1.give('EX1_371') # Hand of Protection
#     #game.player1.give('EX1_384') # Avenging Wrath
#     #game.player1.give('EX1_399') # Gurubashi Berserker
#     #game.player2.give('CS2_005')

# B1 / C1 - Wisp
# B2 / C2 - Target Dummy
# B3 / C3 - Argent Squire
# B4 / C4 - Wisp
# B5 / C5 - Target Dummy
# B6 / C6 - Argent Squire
# B7 / C7 - Wisp
# A01 - Claw
# A02 - Arcane Missiles
# A03 - Pyroblast
# A04 - Azure Drake
# A05 - Summoning Portal
# A06 - Lightspawn
# A07 - Humility
# A08 - Hand of Protection
# A09 - Avenging Wrath
# A10 - Gurubashi Berserker

# Syntax:
# A/B[number_of_card (01..10)]H/B/G/C[number_of_card (00..07)]
# X/H[00]/
# print(interpretDecodedAction('A01H0', game))
# print(interpretDecodedAction('A01B1', game))
# print(interpretDecodedAction('A01B2', game))
# print(interpretDecodedAction('A01B3', game))
# print(interpretDecodedAction('A01B4', game))
# print(interpretDecodedAction('A01B5', game))
# print(interpretDecodedAction('A01B6', game))
# print(interpretDecodedAction('A01B7', game))
# print(interpretDecodedAction('A01G0', game))
# print(interpretDecodedAction('A01C1', game))
# print(interpretDecodedAction('A01C2', game))
# print(interpretDecodedAction('A01C3', game))
# print(interpretDecodedAction('A01C4', game))
# print(interpretDecodedAction('A01C5', game))
# print(interpretDecodedAction('A01C6', game))
# print(interpretDecodedAction('A01C7', game))
# print(interpretDecodedAction('A0100', game))
# print("-------------------------------------------------------------------------------------")
# print(interpretDecodedAction('X00H0',game))
# print(interpretDecodedAction('X00B1',game))
# print(interpretDecodedAction('X00B2',game))
# print(interpretDecodedAction('X00B3',game))
# print(interpretDecodedAction('X00B4',game))
# print(interpretDecodedAction('X00B5',game))
# print(interpretDecodedAction('X00B6',game))
# print(interpretDecodedAction('X00B7',game))
# print(interpretDecodedAction('X00G0',game))
# print(interpretDecodedAction('X00C1',game))
# print(interpretDecodedAction('X00C2',game))
# print(interpretDecodedAction('X00C3',game))
# print(interpretDecodedAction('X00C4',game))
# print(interpretDecodedAction('X00C5',game))
# print(interpretDecodedAction('X00C6',game))
# print(interpretDecodedAction('X00C7',game))
# print(interpretDecodedAction('X0000',game))
# print("-------------------------------------------------------------------------------------")
# print(interpretDecodedAction('H00G0',game))
# print(interpretDecodedAction('H00C1',game))
# print(interpretDecodedAction('H00C2',game))
# print(interpretDecodedAction('H00C3',game))
# print(interpretDecodedAction('H00C4',game))
# print(interpretDecodedAction('H00C5',game))
# print(interpretDecodedAction('H00C6',game))
# print(interpretDecodedAction('H00C7',game))
# print("-------------------------------------------------------------------------------------")
# print(interpretDecodedAction('B01G0',game))
# print(interpretDecodedAction('B01C1',game))
# print(interpretDecodedAction('B01C2',game))
# print(interpretDecodedAction('B01C3',game))
# print(interpretDecodedAction('B01C4',game))
# print(interpretDecodedAction('B01C5',game))
# print(interpretDecodedAction('B01C6',game))
# print(interpretDecodedAction('B01C7',game))
# print(interpretDecodedAction('E0000',game))

# BasicDruid =  ['EX1_169', 'EX1_169', 'CS2_005', 'CS2_005', 'CS2_189', 'CS2_189', 'CS2_120', 'CS2_120', 'CS2_009', 'CS2_009', 'CS2_013', 'CS2_013', 'CS2_007', 'CS2_007', 'CS2_127', 'CS2_127', 'CS2_182', 'CS2_182', 'CS2_119', 'CS2_119', 'DS1_055', 'DS1_055', 'EX1_593', 'EX1_593', 'CS2_200', 'CS2_200', 'CS2_162', 'CS2_162', 'CS2_201', 'CS2_201']
# BasicHunter = ['DS1_185', 'DS1_185', 'CS2_171', 'CS2_171', 'DS1_175', 'DS1_175', 'DS1_184', 'DS1_184', 'CS2_172', 'CS2_172', 'CS2_120', 'CS2_120', 'CS2_141', 'CS2_141', 'CS2_122', 'CS2_122', 'CS2_196', 'CS2_196', 'CS2_127', 'CS2_127', 'DS1_070', 'DS1_070', 'DS1_183', 'DS1_183', 'CS2_119', 'CS2_119', 'CS2_150', 'CS2_150', 'CS2_201', 'CS2_201']
# BasicMage =   ['CFM_623', 'CFM_623', 'CS2_168', 'CS2_168', 'CS2_025', 'CS2_025', 'CS2_172', 'CS2_172', 'EX1_050', 'EX1_050', 'CS2_120', 'CS2_120', 'CS2_023', 'CS2_023', 'CS2_122', 'CS2_122', 'CS2_124', 'CS2_124', 'CS2_029', 'CS2_029', 'CS2_119', 'CS2_119', 'CS2_022', 'CS2_022', 'CS2_179', 'CS2_179', 'EX1_593', 'EX1_593', 'CS2_200', 'CS2_200']
# BasicPaladin= ['CS2_087', 'CS2_087', 'CS1_042', 'CS1_042', 'EX1_371', 'EX1_371', 'CS2_091', 'CS2_091', 'CS2_171', 'CS2_171', 'CS2_089', 'CS2_089', 'CS2_141', 'CS2_141', 'CS2_122', 'CS2_122', 'CS2_147', 'CS2_147', 'CS2_094', 'CS2_094', 'CS2_131', 'CS2_131', 'EX1_593', 'EX1_593', 'CS2_150', 'CS2_150', 'CS2_162', 'CS2_162', 'CS2_222', 'CS2_222']
# BasicPriest = ['CS2_189', 'CS2_189', 'CS1_130', 'CS1_130', 'CS2_235', 'CS2_235', 'CS2_004', 'CS2_004', 'EX1_011', 'EX1_011', 'EX1_192', 'EX1_192', 'CS2_172', 'CS2_172', 'CS2_121', 'CS2_121', 'CS2_234', 'CS2_234', 'EX1_019', 'EX1_019', 'CS2_127', 'CS2_127', 'CS2_182', 'CS2_182', 'CS2_179', 'CS2_179', 'EX1_399', 'EX1_399', 'CS2_201', 'CS2_201']
# BasicRogue =  ['CS2_072', 'CS2_072', 'CS2_074', 'CS2_074', 'CS2_189', 'CS2_189', 'CS1_042', 'CS1_042', 'CS2_075', 'CS2_075', 'CS2_172', 'CS2_172', 'EX1_050', 'EX1_050', 'EX1_581', 'EX1_581', 'CS2_141', 'CS2_141', 'EX1_025', 'EX1_025', 'CS2_147', 'CS2_147', 'CS2_131', 'CS2_131', 'CS2_076', 'CS2_076', 'EX1_593', 'EX1_593', 'CS2_150', 'CS2_150']
# BasicShaman = ['CS2_041', 'CS2_041', 'CS2_037', 'CS2_037', 'CS2_171', 'CS2_171', 'CS2_121', 'CS2_121', 'CS2_045', 'CS2_045', 'CS2_039', 'CS2_039', 'CS2_122', 'CS2_122', 'CS2_124', 'CS2_124', 'CS2_182', 'CS2_182', 'EX1_246', 'EX1_246', 'CS2_179', 'CS2_179', 'CS2_187', 'CS2_187', 'CS2_226', 'CS2_226', 'CS2_200', 'CS2_200', 'CS2_213', 'CS2_213']
# BasicWarlock= ['CS2_168', 'CS2_168', 'CS2_065', 'CS2_065', 'EX1_011', 'EX1_011', 'CS2_142', 'CS2_142', 'CS2_120', 'CS2_120', 'EX1_306', 'EX1_306', 'CS2_061', 'CS2_061', 'CS2_057', 'CS2_057', 'CS2_124', 'CS2_124', 'CS2_182', 'CS2_182', 'CS2_062', 'CS2_062', 'CS2_197', 'CS2_197', 'DS1_055', 'DS1_055', 'CS2_213', 'CS2_213', 'CS2_186', 'CS2_186']
# BasicWarrior= ['CS2_168', 'CS2_168', 'CS2_108', 'CS2_108', 'CS2_121', 'CS2_121', 'CS2_105', 'CS2_105', 'EX1_506', 'EX1_506', 'CS2_106', 'CS2_106', 'CS2_196', 'CS2_196', 'CS2_103', 'CS2_103', 'EX1_084', 'EX1_084', 'CS2_124', 'CS2_124', 'EX1_025', 'EX1_025', 'CS2_179', 'CS2_179', 'EX1_399', 'EX1_399', 'CS2_200', 'CS2_200', 'CS2_162', 'CS2_162']
#
# MidrangeDruid=  ['EX1_169', 'EX1_169', 'AT_037', 'AT_037', 'AT_038', 'EX1_154', 'EX1_154', 'CS2_011', 'CS2_011', 'CS2_013', 'CS2_013', 'EX1_166', 'EX1_166', 'AT_039', 'AT_039', 'EX1_165', 'EX1_165', 'EX1_571', 'EX1_571', 'NEW1_008', 'NEW1_008', 'EX1_005', 'GVG_096', 'GVG_096', 'EX1_284', 'FP1_030', 'BRM_028', 'GVG_110', 'CS2_012', 'CS2_012']
# AggroHunter =   ['LOOT_222', 'LOOT_222', 'LOOT_258', 'LOOT_258', 'UNG_912', 'UNG_912', 'EX1_066', 'UNG_915', 'UNG_915', 'LOOT_413', 'LOOT_413', 'NEW1_031', 'NEW1_031', 'ICC_419', 'ICC_419', 'EX1_539', 'EX1_539', 'EX1_538', 'GIL_828', 'GIL_828', 'LOOT_077', 'DS1_070', 'DS1_070', 'GIL_650', 'EX1_048', 'EX1_048', 'DS1_178', 'EX1_531', 'EX1_534', 'EX1_534']
# MechMage =      ['NEW1_012', 'CS2_024', 'CS2_024', 'GVG_002', 'GVG_002', 'GVG_003', 'CS2_029', 'CS2_029', 'GVG_004', 'GVG_004', 'CS2_033', 'CS2_033', 'EX1_559', 'GVG_082', 'GVG_082', 'GVG_013', 'GVG_013', 'GVG_085', 'GVG_085', 'GVG_006', 'GVG_006', 'GVG_044', 'GVG_044', 'GVG_102', 'GVG_078', 'FP1_030', 'GVG_115', 'GVG_110', 'GVG_096', 'GVG_096']
# ControlPaladin= ['EX1_360', 'EX1_619', 'EX1_619', 'CS2_089', 'EX1_382', 'EX1_382', 'CS2_093', 'CS2_093', 'LOE_017', 'LOE_017', 'CS2_097', 'CS2_097', 'AT_104', 'EX1_354', 'EX1_383', 'NEW1_020', 'NEW1_020', 'EX1_007', 'EX1_007', 'EX1_085', 'EX1_005', 'CS2_179', 'CS2_179', 'EX1_048', 'EX1_564', 'NEW1_041', 'EX1_032', 'EX1_016', 'EX1_298', 'EX1_572']
# ControlPriest = ['EX1_621', 'EX1_621', 'GVG_012', 'GVG_012', 'CS2_235', 'CS2_235', 'CS2_004', 'CS2_004', 'FP1_001', 'FP1_001', 'EX1_622', 'EX1_622', 'EX1_339', 'EX1_339', 'NEW1_020', 'NEW1_020', 'FP1_009', 'CS2_181', 'CS2_181', 'EX1_591', 'EX1_591', 'CS1_112', 'FP1_012', 'FP1_012', 'GVG_014', 'EX1_091', 'AT_132', 'GVG_008', 'GVG_008', 'EX1_572']
# OilRogue =      ['CS2_072', 'CS2_072', 'EX1_145', 'EX1_145', 'CS2_074', 'CS2_074', 'CS2_233', 'CS2_233', 'EX1_124', 'EX1_124', 'EX1_581', 'EX1_581', 'EX1_613', 'EX1_129', 'EX1_129', 'EX1_134', 'EX1_134', 'GVG_022', 'GVG_022', 'CS2_077', 'CS2_077', 'EX1_012', 'CS2_117', 'CS2_117', 'GVG_096', 'NEW1_026', 'NEW1_026', 'EX1_284', 'EX1_284', 'FP1_030']
# MidrangeShaman= ['EX1_245', 'GVG_038', 'GVG_038', 'EX1_565', 'EX1_565', 'CS2_045', 'CS2_045', 'EX1_248', 'EX1_248', 'EX1_259', 'EX1_259', 'EX1_575', 'EX1_246', 'EX1_246', 'EX1_567', 'CS2_042', 'CS2_042', 'NEW1_010', 'EX1_012', 'FP1_002', 'FP1_002', 'EX1_093', 'EX1_093', 'GVG_096', 'GVG_096', 'GVG_069', 'EX1_284', 'EX1_284', 'FP1_030', 'GVG_110']
# DemonZoo =      ['EX1_319', 'EX1_319', 'EX1_316', 'EX1_316', 'CS2_065', 'CS2_065', 'LOE_023', 'LOE_023', 'BRM_006', 'BRM_006', 'EX1_304', 'GVG_045', 'GVG_045', 'FP1_022', 'FP1_022', 'EX1_310', 'EX1_310', 'GVG_021', 'CS2_188', 'CS2_188', 'FP1_002', 'FP1_002', 'NEW1_019', 'NEW1_019', 'FP1_007', 'FP1_007', 'CS2_203', 'EX1_093', 'EX1_093', 'GVG_110']
# MidrangeWarrior=['CS2_108', 'CS2_108', 'EX1_410', 'EX1_410', 'EX1_402', 'EX1_402', 'EX1_603', 'EX1_603', 'BRM_015', 'CS2_106', 'CS2_106', 'EX1_606', 'EX1_606', 'FP1_021', 'FP1_021', 'EX1_407', 'GVG_053', 'GVG_053', 'EX1_414', 'EX1_007', 'EX1_007', 'EX1_005', 'EX1_558', 'FP1_012', 'FP1_012', 'EX1_016', 'EX1_249', 'GVG_110', 'EX1_561', 'EX1_572']
#
#
# FastDruid = ['EX1_169', 'EX1_169', 'EX1_154', 'EX1_154', 'CS2_011', 'CS2_011', 'CS2_013', 'CS2_013', 'EX1_166', 'EX1_166', 'CS2_012', 'CS2_012', 'EX1_165', 'EX1_165', 'EX1_571', 'NEW1_008', 'NEW1_008', 'EX1_573', 'FP1_001', 'EX1_085', 'FP1_005', 'FP1_005', 'EX1_005', 'GVG_096', 'GVG_096', 'EX1_284', 'EX1_558', 'FP1_012', 'EX1_016', 'GVG_110']
# FaceHunter= ['GVG_043', 'GVG_043', 'BRM_013', 'BRM_013', 'NEW1_031', 'NEW1_031', 'EX1_536', 'EX1_536', 'EX1_539', 'EX1_539', 'EX1_538', 'EX1_538', 'CS2_188', 'CS2_188', 'EX1_008', 'EX1_008', 'EX1_029', 'EX1_029', 'FP1_002', 'FP1_002', 'NEW1_019', 'NEW1_019', 'AT_084', 'AT_084', 'EX1_089', 'EX1_089', 'AT_087', 'AT_087', 'CS2_203', 'CS2_203']
# FlamewalkerTempoMage = ['EX1_277', 'EX1_277', 'NEW1_012', 'NEW1_012', 'GVG_001', 'GVG_001', 'CS2_024', 'CS2_024', 'GVG_003', 'GVG_003', 'BRM_002', 'BRM_002', 'CS2_029', 'CS2_029', 'EX1_608', 'EX1_608', 'CS2_032', 'CS2_032', 'EX1_066', 'EX1_066', 'GVG_096', 'GVG_096', 'EX1_284', 'EX1_284', 'FP1_012', 'FP1_012', 'FP1_030', 'EX1_016', 'GVG_110', 'EX1_298']
# MurlocPaladin = ['GVG_058', 'GVG_058', 'EX1_382', 'EX1_382', 'GVG_059', 'GVG_061', 'GVG_061', 'CS2_093', 'CS2_093', 'LOE_017', 'CS2_097', 'BRM_001', 'EX1_354', 'LOE_026', 'FP1_001', 'CS2_173', 'CS2_173', 'NEW1_019', 'EX1_096', 'EX1_096', 'EX1_507', 'EX1_507', 'EX1_595', 'EX1_062', 'GVG_096', 'GVG_096', 'GVG_069', 'GVG_069', 'FP1_012', 'GVG_110']
# DragonPriest = ['CS2_235', 'CS2_235', 'CS2_004', 'CS2_004', 'BRM_004', 'BRM_004', 'EX1_622', 'EX1_622', 'CS2_234', 'AT_116', 'AT_116', 'FP1_023', 'GVG_010', 'GVG_010', 'CS1_112', 'CS1_112', 'GVG_014', 'NEW1_020', 'BRM_033', 'BRM_033', 'BRM_020', 'AT_017', 'AT_017', 'EX1_284', 'EX1_284', 'BRM_034', 'BRM_034', 'AT_123', 'BRM_031', 'EX1_572']
#
# a = 0