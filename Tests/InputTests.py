import copy

import numpy as np
from GameState.HandCards import HandCard
from main import mulliganRandomChoice, setup_game



def check_basic_features_weapon(item, basicFeatures, cost,powerUp,isMinion,isSpell,
                                isWeapon,discount,currentDurability,
                                currentAttack,baseDurability):

    ## basicFeatures expected values

    if basicFeatures[0] != cost:# cost
        print(f"{item} COST NOT EQUAL")
    if basicFeatures[1] != powerUp: # power up
        print(f"{item} IS POWERED UP NOT EQUAL")
    if basicFeatures[2] != isMinion: # is minion
        print(f"{item} IS MINION NOT EQUAL")
    if basicFeatures[3] != isSpell: # is spell
        print(f"{item} IS SPELL NOT EQUAL")
    if basicFeatures[4] != isWeapon: # is weapon
        print(f"{item} IS WEAPON NOT EQUAL")
    if basicFeatures[5] != discount :# discount
        print(f"{item} DISCOUNT NOT EQUAL")
    if basicFeatures[51] != currentDurability: # current durability
        print(f"{item} CURRENT DURABILITY NOT EQUAL")
    if basicFeatures[52] != currentAttack: # current attack
        print(f"{item} CURRENT ATTACK NOT EQUAL")
    if basicFeatures[53] != baseDurability: # base durability ( for sure )
        print(f"{item} BASE DURABILITY NOT EQUAL")

def check_basic_features_minion(item, basicFeatures,
                                cost, powerUp,
                                isMinion,isSpell,
                                isWeapon,discount,
                                expectedFeatures):

    ## basicFeatures expected values
    if basicFeatures[0] != cost:# cost
        print(f" {item} COST NOT EQUAL")
    if basicFeatures[1] != powerUp: # power up
        print(f" {item} IS POWERED UP NOT EQUAL")
    if basicFeatures[2] != isMinion: # is minion
        print(f" {item} IS MINION NOT EQUAL")
    if basicFeatures[3] != isSpell: # is spell
        print(f" {item} IS SPELL NOT EQUAL")
    if basicFeatures[4] != isWeapon: # is weapon
        print(f" {item} IS WEAPON NOT EQUAL")
    if basicFeatures[5] != discount :# discount
        print(f" {item} DISCOUNT NOT EQUAL")

    for i in range(51, 83):
        if basicFeatures[i] != expectedFeatures[i]: # is weapon
            print(f" {item} basic feature at index {i} is invalid ")



def check_plane(item, battlecryFeatures, expectedFeatures):
    for i in range(len(expectedFeatures)):
        if battlecryFeatures[i] != expectedFeatures[i]:
            print(f"Index {i} of battlecrySpell feature is not valid for CHECKED item: {item}")



def checkForNumpyZeros(item, plane):
    if not np.array_equal(plane, np.zeros(169)):
        print(f" {item} The plane should be filled with zeros since it has not have that effect assigned")


def test_fiery_war_axe():
    #### BASIC FEATURES ####
    game = setup_game()
    mulliganRandomChoice(game)
    game.player1.discard_hand()
    game.player2.discard_hand()

    game._end_turn()
    #######
    card = game.player2.give("CS2_106")
    test = HandCard(card)
    planes = test.encode_state_DEBUG()
    game.player2.max_mana = 10

    ###### CHECK FUNCTION FOR WEAPON ( TAKES EXPECTED OUTPUT VALUES )
    check_basic_features_weapon("CS2_106", planes[0],
                                cost=3, powerUp=0, isMinion=0, isSpell=0,
                                isWeapon=1, discount=0, currentDurability=2,
                                currentAttack=3, baseDurability=2)

    #### Initial other null planes check
    for plane in planes[1:]:
        checkForNumpyZeros("CS2_106", plane)


    #### problemy z discountem przy nowszych karcioszkach
    cardToDecreaseCost = game.player2.give("CS3_008")

    cardToDecreaseCost.play()

    game.end_turn()
    game.end_turn()


    game.player2.max_mana = 10
    card.play()

    testAfterPlay = HandCard(card)
    planes = testAfterPlay.encode_state_DEBUG()
    check_basic_features_weapon("CS2_106",planes[0],
                                cost=2, powerUp=0 , isMinion=0,isSpell=0,
                                isWeapon=1,discount=0,currentDurability=2,
                                currentAttack=3,baseDurability=2)

    ### check for attack buff and durability buff +1/+1

    game.end_turn()
    game.end_turn()
    bloodsailCultist = game.player2.give("OG_315")
    bloodsailCultist.play()

    test = HandCard(card)
    planes = test.encode_state_DEBUG()
    ### Base Durability to w sumie max durability
    check_basic_features_weapon("CS2_106",
                                planes[0],
                                cost=3, powerUp=0 , isMinion=0,isSpell=0,
                                isWeapon=1,discount=0,currentDurability=3,
                                currentAttack=4,baseDurability=2)



def test_frostwolf_warlord():
    game = setup_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    mulliganRandomChoice(game)
    game.end_turn()
    #######

    game.current_player.max_mana = 10
    card0 = game.current_player.give("BRM_028")
    card1 = game.current_player.give("EX1_506")
    card0.play()

    game.end_turn()
    game.end_turn()


    card1.play()
    # card2 = game.current_player.give("EX1_506")
    # card2.play()
    frostwolf = game.current_player.give("CS2_226")
    frostwolf.play()

    test = HandCard(frostwolf)
    planes = test.encode_state_DEBUG()

    expectedPlaneValue = copy.deepcopy(planes[0])
    expectedPlaneValue[51] = 8
    expectedPlaneValue[52] = 8
    check_basic_features_minion("CS2_226",basicFeatures= planes[0],
                                cost=5,powerUp=0,isMinion=1,
                                isSpell=0,isWeapon=0,discount=0,expectedFeatures=expectedPlaneValue)

    battlecryFeatures = copy.deepcopy(planes[1])
    battlecryFeatures[0] = 2 # 4 miniony na boardzie = +4 health
    battlecryFeatures[1] = 2 # 4 miniony na boardzie = +4 attack
    check_plane("CS2_226",battlecryFeatures=planes[1],expectedFeatures=battlecryFeatures)
    ## zczekować jeszcze battlecry effect

def test_sludge_belcher():
    game = setup_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    mulliganRandomChoice(game)
    game.end_turn()

    ######
    game.current_player.max_mana = 10
    sludge = game.current_player.give("FP1_012")
    sludge.play()

    test = HandCard(sludge)
    planes = test.encode_state_DEBUG()

    deathrattleFeatures = copy.deepcopy(planes[4])
    deathrattleFeatures[113] = 1
    deathrattleFeatures[114] = 0

    check_plane("FP1_012",planes[4],deathrattleFeatures)


def test_blood_imp():

    game = setup_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    mulliganRandomChoice(game)
    game.end_turn()

    ######
    game.current_player.max_mana = 10
    bloodimp = game.current_player.give("CS2_059")
    bloodimp.play()

    test = HandCard(bloodimp)
    planes = test.encode_state_DEBUG()

    eot = copy.deepcopy(planes[2])
    eot[0] = 1
    eot[6] = 1
    check_plane("CS2_059",planes[2],eot)