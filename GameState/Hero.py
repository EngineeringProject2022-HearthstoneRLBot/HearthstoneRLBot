import fireplace
from fireplace.actions import SetTag, Silence, Heal, Hit, Destroy, GainArmor, Draw, Discard, Summon, Bounce
from fireplace.card import Card
from fireplace.dsl import LazyValue, RandomEntourage
from hearthstone.enums import Race, GameTag, PlayReq

from HearthstoneRLBot.GameState.HandCards import getTargetedActionDetails


class Hero:
    def __init__(self):
        self.currentHeroState = {}

    def HeroDecode(self, hero):
        self.currentHeroState["health"] = hero.health
        self.currentHeroState["attack"] = hero.atk
        #currentHeroState["sleeping"] = hero.???
        self.currentHeroState["frozen"] = int(hero.frozen)
        self.currentHeroState["rush"] = int(hero.rush)
        self.currentHeroState["taunt"] = int(hero.taunt)
        #currentHeroState["divineShield"] = int(hero.???)
        self.currentHeroState["isBuffed"] = 1 if len(hero.buffs) else 0
        #currentHeroState["isBuffed"] = int(hero.powered_up) jedno albo drugie w sumie nie wiem
        #currentHeroState["stealth"] = ???
        self.currentHeroState["windFury"] = hero.windfury
        self.currentHeroState["hasWeapon"] = 0 if hero.controller.weapon is None else 1
        self.currentHeroState["isImmune"] = int(hero.immune)
        self.currentHeroState["isImmuneWhileAtk"] = int(hero.immune_while_attacking)
        self.currentHeroState["armor"] = hero.armor
        self.currentHeroState["weaponId"] = 0 if hero.controller.weapon is None else hero.controller.weapon.data.card_id
        self.currentHeroState["weaponPoisonous"] = 0 if hero.controller.weapon is None else int(hero.controller.weapon.data.poisonous)
        self.currentHeroState["weaponAtt"] = 0 if hero.controller.weapon is None else hero.controller.weapon.data.atk
        self.currentHeroState["weaponDurability"] = 0 if hero.controller.weapon is None else hero.controller.weapon.data.durability
        #currentHeroState["weaponBuff"] = nie wiem co tu moze byc tbh
        self.currentHeroState["canAttack"] = 0 if hero.num_attacks == hero.max_attacks else 1 #jeszcze tu nie jestem tego pewny jak cos


        heroPower = {}
        #Hero power needs to be implemented!
        if str(hero) != "Thrall":
            for x in hero.power.data.scripts.activate: #.activate albo .entourage
                heroPower["AlwaysGet"] = 1
                getTargetedActionDetails(x, heroPower, hero)
        else:
            heroPower["AlwaysGet"] = 1
            heroPower["FromEntourage"] = 1
            sum_health = 0
            sum_atk = 0
            sum_cost = 0
            for y in hero.power.data.scripts.entourage:
                card = Card(y)
                sum_atk += card.atk
                sum_health += card.health
                sum_cost += card.cost
            heroPower["SummonedAvgHealth"] = sum_health / len(hero.power.data.scripts.entourage)
            heroPower["SummonedAvgAttack"] = sum_atk / len(hero.power.data.scripts.entourage)
            heroPower["SummonedAvgCost"] = sum_cost / len(hero.power.data.scripts.entourage)
            heroPower["SummonedCalculatedValue"] = 1
        print("")