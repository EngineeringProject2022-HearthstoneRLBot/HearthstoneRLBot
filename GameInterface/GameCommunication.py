import random

import numpy as np
from fireplace.exceptions import InvalidAction
from fireplace.targeting import is_valid_target

MAX_BOARD = 15 # ustaw 8 aby nie było wyjątków

def checkValidHandCard(allychars, enemychars, card):
    cardindexes = np.zeros(17)

    if card.must_choose_one: # randomowe wybranie karty do walidowania...
        card = card.choose_cards[0]
    if card.cant_play:
        return cardindexes
    if hasattr(card, 'is_playable') and not card.is_playable():
        return cardindexes
    elif hasattr(card, 'is_usable') and not card.is_usable():
        return cardindexes

    if not card.requires_target():
        cardindexes[16] = 1
        return cardindexes

    for i, character in enumerate(allychars):
        if character \
                and i < MAX_BOARD \
                and is_valid_target(card, character):
            cardindexes[i] = 1
    for i, character in enumerate(enemychars):
        if character \
                and i < MAX_BOARD \
                and is_valid_target(card, character):
            if hasattr(card, 'attack_targets'):
                if character in card.attack_targets:
                    cardindexes[8 + i] = 1
            else:
                cardindexes[8+i] = 1

    return cardindexes


def checkValidCharacter(enemychars, character):
    charindexes = np.zeros(8)

    if not character.can_attack():
        return charindexes

    for i, enemycharacter in enumerate(enemychars):
        if enemycharacter and character.can_attack(enemycharacter):
            charindexes[i] = 1
    return charindexes


def checkValidActions(game):
    actionsindexes = np.zeros(252)
    player = game.current_player
    enemy = player.opponent
    allychars = player.characters
    enemychars = enemy.characters

    for i, handcard in enumerate(player.hand):
        if handcard and i < MAX_BOARD: # gra pozwala miec wiecej niz 8 characterow
            actionsindexes[(i * 17):((i + 1) * 17)] = checkValidHandCard(allychars, enemychars, handcard)
    actionsindexes[170:187] = checkValidHandCard(allychars, enemychars, player.hero.power)
    for i, character in enumerate(allychars):
        if character and i < MAX_BOARD: # gra pozwala miec wiecej niz 8 characterow XD
            actionsindexes[(187+i*8):(187+(i+1)*8)] = checkValidCharacter(enemychars, character)
    actionsindexes[251] = 1

    return actionsindexes

def playRandomChooseOne(card):
    target = None
    card = random.choice(card.choose_cards)
    if card.requires_target():
        target = random.choice(card.targets)
    card.play(target=target)


def useCard(player, enemy, action):
    card = player.hand[int(action / 17)]

    choose = None
    if card.must_choose_one: # jesli jest i choose one to biore randomowo
        #card = card.choose_cards[0]
        choose = card.choose_cards[0].data.card_id

    cardtarget = action % 17
    targetchar = None
    if cardtarget < 8:
        targetchar = player.characters[cardtarget]
    elif cardtarget < 16:
        targetchar = enemy.characters[cardtarget-8]
    if card.must_choose_one:
        card.play(choose=choose, target=targetchar)
    else:
        card.play(target=targetchar)
    card.cant_play = True # inaczej w nieskonczonosc gram ta sama karte...


def usePower(player, enemy, action):
    power = player.hero.power
    powertarget = action % 17
    targetchar = None
    if powertarget < 8:
        targetchar = player.characters[powertarget]
    elif powertarget < 16:
        targetchar = enemy.characters[powertarget-8]
    power.use(target=targetchar)


def playTurn(game, output):
    player = game.current_player
    while player.choice:
        choice = random.choice(player.choice.cards)
        print("Choosing card %r" % (choice))
        player.choice.choose(choice)

    filteredoutput = np.multiply(output, checkValidActions(game))
    action = filteredoutput.argmax() # tu można by brać randomowego maxa, a nie pierwszego
    return playTurnSparse(game, action)


def checkValidActionsSparse(game):
    return [i for i, x in enumerate(checkValidActions(game)) if x == 1]


def playTurnSparse(game, action):
    game.randomOccured = False
    player = game.current_player
    enemy = player.opponent
    if action == 251:
        game.end_turn()
    elif action < 170:
        useCard(player, enemy, action)
    elif action < 187:
        usePower(player, enemy, action)
    else:
        minion = player.characters[int((action-187)/8)]
        miniontarget = (action-187) % 8
        minion.attack(enemy.characters[miniontarget])

    while player.choice:
        player.choice.choose(random.choice(player.choice.cards))

    if game.randomOccured:
        return 1
    else:
        return 0
