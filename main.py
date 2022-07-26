import copy
import operator
import sys
from copy import deepcopy
from logging import getLogger

#from venv import logger

import fireplace
import numpy as np

from fireplace import cards

from fireplace import cards, logging

from fireplace.exceptions import GameOver
import os.path
import random
from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List
from xml.etree import ElementTree
from hearthstone.enums import CardClass, CardType  # noqa
from collections.abc import Callable
# Autogenerate the list of cardset modules
from GameCommunication import playTurn
from GameState import HandCard
from GameState import Hero
import HearthstoneRLBot.Tests.InputTests
from HearthstoneRLBot.Tests import InputTests
from Model import Resnet

_cards_module = os.path.join(os.path.dirname(__file__), "cards")
CARD_SETS = [cs for _, cs, ispkg in iter_modules([_cards_module]) if ispkg]

from GameState.GameState import GameState

sys.path.append("..")

class CardList(list):
    def __contains__(self, x):
        for item in self:
            if x is item:
                return True
        return False

    def __getitem__(self, key):
        ret = super().__getitem__(key)
        if isinstance(key, slice):
            return self.__class__(ret)
        return ret

    def __int__(self):
        # Used in Kettle to easily serialize CardList to json
        return len(self)

    def contains(self, x):
        """
        True if list contains any instance of x
        """
        for item in self:
            if x == item:
                return True
        return False

    def index(self, x):
        for i, item in enumerate(self):
            if x is item:
                return i
        raise ValueError

    def remove(self, x):
        for i, item in enumerate(self):
            if x is item:
                del self[i]
                return
        raise ValueError

    def exclude(self, *args, **kwargs):
        if args:
            return self.__class__(e for e in self for arg in args if e is not arg)
        else:
            return self.__class__(e for k, v in kwargs.items() for e in self if getattr(e, k) != v)

    def filter(self, **kwargs):
        return self.__class__(e for k, v in kwargs.items() for e in self if getattr(e, k, 0) == v)


def random_draft(card_class: CardClass, exclude=[]):
    """
    Return a deck of 30 random cards for the \a card_class
    """
    from fireplace import cards
    from fireplace.deck import Deck

    deck = []
    collection = []
    # hero = card_class.default_hero

    for card in cards.db.keys():
        if card in exclude:
            continue
        cls = cards.db[card]
        if not cls.collectible:
            continue
        if cls.type == CardType.HERO:
            # Heroes are collectible...
            continue
        if cls.card_class and cls.card_class not in [card_class, CardClass.NEUTRAL]:
            # Play with more possibilities
            continue
        collection.append(cls)

    while len(deck) < Deck.MAX_CARDS:
        card = random.choice(collection)
        if deck.count(card.id) < card.max_count_in_deck:
            deck.append(card.id)

    return deck


def random_class():
    return CardClass(random.randint(2, 10))


def get_script_definition(id):
    """
    Find and return the script definition for card \a id
    """
    for cardset in CARD_SETS:
        module = import_module("fireplace.cards.%s" % (cardset))
        if hasattr(module, id):
            return getattr(module, id)


def entity_to_xml(entity):
    e = ElementTree.Element("Entity")
    for tag, value in entity.tags.items():
        if value and not isinstance(value, str):
            te = ElementTree.Element("Tag")
            te.attrib["enumID"] = str(int(tag))
            te.attrib["value"] = str(int(value))
            e.append(te)
    return e


def game_state_to_xml(game):
    tree = ElementTree.Element("HSGameState")
    tree.append(entity_to_xml(game))
    for player in game.players:
        tree.append(entity_to_xml(player))
    for entity in game:
        if entity.type in (CardType.GAME, CardType.PLAYER):
            # Serialized those above
            continue
        e = entity_to_xml(entity)
        e.attrib["CardID"] = entity.id
        tree.append(e)

    return ElementTree.tostring(tree)


def weighted_card_choice(source, weights: List[int], card_sets: List[str], count: int):
    """
    Take a list of weights and a list of card pools and produce
    a random weighted sample without replacement.
    len(weights) == len(card_sets) (one weight per card set)
    """

    chosen_cards = []

    # sum all the weights
    cum_weights = []
    totalweight = 0
    for i, w in enumerate(weights):
        totalweight += w * len(card_sets[i])
        cum_weights.append(totalweight)

    # for each card
    for i in range(count):
        # choose a set according to weighting
        chosen_set = bisect(cum_weights, random.random() * totalweight)

        # choose a random card from that set
        chosen_card_index = random.randint(0, len(card_sets[chosen_set]) - 1)

        chosen_cards.append(card_sets[chosen_set].pop(chosen_card_index))
        totalweight -= weights[chosen_set]
        cum_weights[chosen_set:] = [x - weights[chosen_set] for x in cum_weights[chosen_set:]]

    return [source.controller.card(card, source=source) for card in chosen_cards]


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


from fireplace.player import Player
from fireplace.game import BaseGame, CoinRules, Game


class BaseTestGame(CoinRules, BaseGame):
    def start(self):
        super().start()
        self.player1.max_mana = 10
        self.player2.max_mana = 10


def _random_class():
    return CardClass(random.randint(2, 10))


def init_game(class1=None, class2=None, exclude=(), game_class=BaseTestGame):
    # log.info("Initializing a new game")
    if class1 is None:
        class1 = _random_class()
    if class2 is None:
        class2 = _random_class()
    player1 = Player("Player1", *_draft(class1, exclude))
    player2 = Player("Player2", *_draft(class2, exclude))
    game = game_class(players=(player1, player2))
    return game


_draftcache = {}


def _empty_mulligan(game):
    for player in game.players:
        if player.choice:
            player.choice.choose()


BLACKLIST = (
    "GVG_007",  # Flame Leviathan
    "AT_022",  # Fist of Jaraxxus
    "AT_130",  # Sea Reaver
)


def _draft(card_class, exclude):
    # random_draft() is fairly slow, this caches the drafts
    if (card_class, exclude) not in _draftcache:
        _draftcache[(card_class, exclude)] = random_draft(card_class, exclude + BLACKLIST)
    return _draftcache[(card_class, exclude)], card_class.default_hero


def prepare_game(*args, **kwargs):
    game = init_game(*args, **kwargs)
    game.start()
    _empty_mulligan(game)

    return game


def fireball_test():
    game = prepare_game()

    game.player1.discard_hand()
    game.player2.discard_hand()
    for i in range(29):
        moon = game.player1.give("CS2_008")
        moon.play(target=game.player1.hero)
    # fireball
    fire = game.player2.give("CS2_029")
    for i in range(7):
        # whisp
        a = game.player1.give("CS2_231")
        a.play()
    game.end_turn()
    for i in range(29):
        moon = game.player2.give("CS2_008")
        moon.play(target=game.player2.hero)
    for i in range(7):
        # whisp
        a = game.player2.give("CS2_231")
        a.play()
    # try:
    #     fire.play(target=game.player1.hero)
    # except fireplace.exceptions.GameOver:
    #     print("g")
    return game


def test_cogmaster():
    game = prepare_game()

    # frostwolf = game.player1.give("CS2_226")
    # HandCard(frostwolf)
    # crab = game.player1.give("NEW1_017")
    # HandCard(crab)
    # silence = game.player1.give("EX1_332")
    # #  HandCard(silence)
    # frog = game.player1.give("EX1_103")
    # arge = game.player1.give("EX1_362")
    # #HandCard(arge)
    # #HandCard(frog)
    # amani = game.player1.give("EX1_393")
    # HandCard(amani)
    # edwin = game.player1.give("EX1_613")
    # HandCard(edwin)
    # baron = game.pla1.give("EX1_249")
    # HandCard(baron)
    # amani.play()
    # edwin.play()
    # comboCard2 = game.player1.give("AT_028")
    # comboCard2.play()
    # HandCard(comboCard2)
    #
    #
    # comboCard = game.player1.give("EX1_131")
    # comboCard.play()
    # HandCard(comboCard)
    #
    # snowchugger = game.player1.give("GVG_002")
    # snowchugger.play()
    # HandCard(snowchugger)
    #
    #
    # armorsmith = game.player1.give("CFM_756")
    # armorsmith.play()
    # HandCard(armorsmith)

    # shadowstep = game.player1.give("EX1_144")
    # HandCard(shadowstep)

    # animalCompanion = game.player1.give("NEW1_031")
    # HandCard(animalCompanion)
    # animalCompanion.play(animalCompanion)

    # abusive = game.player1.give("CS2_188")
    # HandCard(abusive)
    # darkBargain = game.player1.give("AT_025")
    # HandCard(darkBargain)
    # soulFire = game.player1.give("EX1_308")
    # HandCard(soulFire)
    # shieldSlam = game.player1.give("EX1_410")
    # HandCard(shieldSlam)
    # SHKnight = game.player1.give("CS2_151")
    # HandCard(SHKnight)
    # novEng = game.player1.give("EX1_015")
    # shieldBlock = game.player1.give("EX1_606")
    # HandCard(shieldBlock)
    # naturalize = game.player1.give("EX1_161")
    # HandCard(novEng)
    # HandCard(naturalize)
    # mechWarper = game.player1.give("GVG_006")
    # HandCard(mechWarper)
    # crab = game.player1.give("NEW1_017")
    # stormpike = game.player1.give("CS2_150")
    # earthenring = game.player1.give("CS2_117")
    # frostelem = game.player1.give("EX1_283")
    # arge = game.player1.give("EX1_362")
    # frog = game.player1.give("EX1_103")
    # shat = game.player1.give("EX1_019")
    # frostwolf = game.player1.give("CS2_226")
    # anima = game.player1.give("CS2_059")
    # anima2 = game.player1.give("EX1_298")
    # anima3 = game.player1.give("CS2_117")
    # anima4 = game.player1.give("CS2_057")
    # anima5 = game.player1.give("FP1_013")
    # anima6 = game.player1.give("CS2_062")
    # anima7 = game.player2.give("EX1_349")
    # anima8 = game.player2.give("LOE_024t")
    # anima9 = game.player2.give("Mekka2")
    # anima10 = game.player2.give("Mekka3")
    # x=HandCard(anima)
    # y=HandCard(anima2)
    # z=HandCard(anima3)
    # a=HandCard(anima4)
    # b=HandCard(anima5)
    # d=HandCard(anima6)
    # i=HandCard(anima7)
    # e=HandCard(anima8)
    # f=HandCard(anima9)
    # g=HandCard(anima10)
    # frost = game.player1.give("CS2_226")
    # HandCard(frost)
    # argus = game.player1.give("EX1_093")
    # div = game.player1.give("CS2_236")
    # bloodsail= game.player1.give("NEW1_018")
    # bchampion = game.player1.give("EX1_355")
    # innerFire = game.player1.give("CS1_129")
    # aldor = game.player1.give("EX1_382")
    # frog.play()
    # HandCard(innerFire)
    # innerFire.play(target=frog)
    # whelp = game.player1.give("BRM_004")
    # CS1_129 inner fire
    # CS2_236 divine spirit
    # EX1_382 aldor
    # EX1_355 blessed champion
    # BRM_004 Twilight Whelp
    # EX1_161 Naturalize
    # EX1_103 frog
    # EX1_019 shat
    # CS2_226 frost
    # EX1_093 argus
    # CFM_756 alley armorsmith
    # cogmaster.play()
    # assert cogmaster.atk == 6
    # dummy = game.player1.give("CS2_029")
    # dummy.play()

    card_list = [
        "CS2_106", # Fiery war axe
        "EX1_308", # Soulfire
        "NEW1_031", # Animal Companion
        "EX1_613",
        "AT_028",
        "NEW1_037"
        "GVG_099",
        "GVG_104",
        "FP1_001",
        "FP1_029",
        "AT_122",
        "AT_040",
        "AT_026",
        "BRM_020",
        "BRM_005",
        "LOE_073",
        "EX1_004",
        "EX1_597",
        "BT_493",
        "BT_761",
        "EX1_575",
        "GVG_089",
        "GVG_039",
        "CFM_639",
        "GVG_020",
        "OG_286",
        "CFM_654",
        "OG_173",
        "FP1_003",
        "CS2_059",
        "BRM_028",
        "KAR_044",
        "OG_200",
        "FP1_005",
        "FP1_027",
        "CFM_609",
        "GVG_111",
        "EX1_006",
        "EX1_341",
        "LOE_007t",
        "EX1_102",
        "AT_073",
        "GVG_103",
        "GVG_077",
        "FP1_013",
        "GVG_076",
        "LOE_115",
        "LOOT_170",
        "EX1_573",
        "CS2_008",
        "EX1_160",
        "NEW1_007",
        "EX1_571",
        "EX1_578",
        "EX1_506",
        "EX1_277"
    ]
    game.player1.discard_hand()
    cardList = []
    for item in card_list:
        print(item)
        try:
            card = game.player1.give(item)
            cardList.append(HandCard(card))
            test = HandCard(card)
            test.encode_state()
        except KeyError:
            print('NIE MA')

        game.player1.discard_hand()

    # frost = game.player1.give("CS2_226")
    # argus = game.player1.give("EX1_093")
    # div = game.player1.give("CS2_236")
    # bloodsail= game.player1.give("NEW1_018")
    # bchampion = game.player1.give("EX1_355")
    # innerFire = game.player1.give("CS1_129")
    # aldor = game.player1.give("EX1_382")
    # frog.play()
    # HandCard(innerFire)
    # innerFire.play(target=frog)
    # whelp = game.player1.give("BRM_004")
    # CS1_129 inner fire
    # CS2_236 divine spirit
    # EX1_382 aldor
    # EX1_355 blessed champion
    # BRM_004 Twilight Whelp
    # EX1_161 Naturalize
    # EX1_103 frog
    # EX1_019 shat
    # CS2_226 frost
    # EX1_093 argus
    # CFM_756 alley armorsmith
    # cogmaster.play()
    # assert cogmaster.atk == 6
    # dummy = game.player1.give("CS2_029")
    # dummy.play()

    # frost = game.player1.give("NEW1_018")
    # get_script_definition("CS2_226")
    # frost.play()
    # theFrost = HandCard(frost)
    # theFrost.play = frost.data.scripts.play
    # theFrost.mapToInput()
    # # assert cogmaster.atk == 3
    # humility = game.player1.give("EX1_360")
    # humility.play(target=cogmaster)
    # # assert cogmaster.atk == 3
    # dummy.destroy()
    # # assert cogmaster.atk == 1
    # game.player1.give("GVG_093").play()
    # assert cogmaster.atk == 3
    # blessedchamp = game.player1.give("EX1_355")
    # blessedchamp.play(target=cogmaster)
    # assert cogmaster.atk == 4

def testGame(game):
    try:
        while True:
            player = game.current_player
            current = GameState(game)
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

def mulliganRandomChoice(game):
    for player in game.players:
        current = GameState(game)
        mull_count = random.randint(0, len(player.choice.cards))
        cards_to_mulligan = random.sample(player.choice.cards, mull_count)
        player.choice.choose(*cards_to_mulligan)

def networkInputTesting():
    while True:
        try:
            game = setup_game()
            mulliganRandomChoice(game)
            while True:
                playTurn(game, np.random.rand(252))
        except GameOver:
            print("Game ended")

            while True:
                player = game.current_player
                current = GameState(game)
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
                                print("Choosing card %r" % (choice))
                                player.choice.choose(choice)
                            continue
                    for character in player.characters:
                        if character.can_attack():
                            character.attack(random.choice(character.targets))
                            if character.buffs:
                                print("gay")
                    break
                    game.end_turn()


def continousTesting():
    while True:
        try:
            game = setup_game()
            mulliganRandomChoice(game)
            testGame(game)
        except GameOver:
            print("Game ended")


def main():
    gameStates = []
    logger = logging.log
    logger.disabled = True
    logger.propagate = False
    cards.db.initialize()
    InputTests.test_sludge_belcher()
    InputTests.test_fiery_war_axe()
    InputTests.test_frostwolf_warlord()
    InputTests.test_blood_imp()
    continousTesting()

    networkInputTesting()
    #continousTesting()

    fireball_test()
    #myNetwork = Resnet.Network()
    #model = myNetwork.getModel()
    test_cogmaster()



# test1
if __name__ == "__main__":
    main()
