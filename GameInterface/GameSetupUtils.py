import random

from fireplace.game import CoinRules, BaseGame
from fireplace.player import Player
from fireplace.utils import random_draft
from hearthstone.enums import CardClass


class BaseTestGame(CoinRules, BaseGame):
    def start(self):
        super().start()
        self.player1.max_mana = 10
        self.player2.max_mana = 10


def mulliganRandomChoice(game):
    for player in game.players:
        mull_count = random.randint(0, len(player.choice.cards))
        cards_to_mulligan = random.sample(player.choice.cards, mull_count)
        player.choice.choose(*cards_to_mulligan)


def prepare_game(*args, **kwargs):
    game = init_game(*args, **kwargs)
    game.start()
    _empty_mulligan(game)
    return game


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


def _empty_mulligan(game):
    for player in game.players:
        if player.choice:
            player.choice.choose()


def random_class():
    return CardClass(random.randint(2, 10))


def _random_class():
    return CardClass(random.randint(2, 10))


_draftcache = {}

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
