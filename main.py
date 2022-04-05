import sys
from fireplace import cards
from fireplace.exceptions import GameOver
from fireplace.utils import play_full_game
import os.path
import random
from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List
from xml.etree import ElementTree

from hearthstone.enums import CardClass, CardType  # noqa

# Autogenerate the list of cardset modules
from GameState import HandCard

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

    deck1 = random_draft(CardClass.MAGE)
    deck2 = random_draft(CardClass.WARRIOR)
    player1 = Player("Player1", deck1, CardClass.MAGE.default_hero)
    player2 = Player("Player2", deck2, CardClass.WARRIOR.default_hero)

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
	#log.info("Initializing a new game")
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

def test_cogmaster():
    game = prepare_game()
    cogmaster = game.player1.give("NEW1_018")
    #cogmaster.play()
    #assert cogmaster.atk == 6
    dummy = game.player1.give("CS2_029")
    #dummy.play()
    frost = game.player1.give("NEW1_018")
    get_script_definition("CS2_226")
    frost.play()
    theFrost = HandCard(frost)
    theFrost.play=frost.data.scripts.play
    theFrost.mapToInput()
    #assert cogmaster.atk == 3
    humility = game.player1.give("EX1_360")
    humility.play(target=cogmaster)
    #assert cogmaster.atk == 3
    dummy.destroy()
    #assert cogmaster.atk == 1
    game.player1.give("GVG_093").play()
    assert cogmaster.atk == 3
    blessedchamp = game.player1.give("EX1_355")
    blessedchamp.play(target=cogmaster)
    assert cogmaster.atk == 4


def main():

    gameStates = []
    cards.db.initialize()
    test_cogmaster()
    game = setup_game()
    try:
        for player in game.players:
            current = GameState(game)
            # 1. Tutaj ustawić do current karty do wyboru
            print("Can mulligan %r" % player.choice.cards)
            mull_count = random.randint(0, len(player.choice.cards))
            cards_to_mulligan = random.sample(player.choice.cards, mull_count)
            player.choice.choose(*cards_to_mulligan)
            gameStates.append(current)

        while True:
            player = game.current_player

            current = GameState(game)
            # 2. Tutaj do current wrzucić aktualny stan gry
            while True:
                heropower = player.hero.power
                if heropower.is_usable() and random.random() < 0.1:
                    if heropower.requires_target():
                        heropower.use(target=random.choice(heropower.targets))
                    else:
                        heropower.use()
                    # 3. Tutaj do current wrzuć nowy stan gry (po użyciu umiejętności)
                    continue

                # iterate over our hand and play whatever is playable
                for card in player.hand:
                    if card.is_playable() and random.random() < 0.5:
                        target = None
                        if card.must_choose_one:
                            card = random.choice(card.choose_cards)
                        if card.requires_target():
                            target = random.choice(card.targets)
                        print("Playing %r on %r" % (card, target))
                        card.play(target=target)

                        # 4. Tutaj do current wrzuć nowy stan gry (po użyciu karty)

                        if player.choice:
                            choice = random.choice(player.choice.cards)
                            print("Choosing card %r" % (choice))
                            player.choice.choose(choice)
                        # 5. Tutaj do current wrzuć nowy stan gry (po użyciu karty i wyborze)
                        continue

                # Randomly attack with whatever can attack
                for character in player.characters:
                    if character.can_attack():
                        character.attack(random.choice(character.targets))
                        if character.buffs:
                            print("gay")

                    # 6. Tutaj do current wrzuć nowy stan gry (po ataku)

                break

            game.end_turn()
    except GameOver:
        print("Game ended");

#test1
if __name__ == "__main__":
    main()
