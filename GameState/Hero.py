import fireplace
from fireplace.actions import SetTag, Silence, Heal, Hit, Destroy, GainArmor, Draw, Discard, Summon, Bounce
from fireplace.card import Card
from fireplace.dsl import LazyValue, RandomEntourage
from hearthstone.enums import Race, GameTag, PlayReq
import numpy as np

from GameState.HandCards import getTargetedActionDetails, encode_targets, encode_complex_plane, getTimes, \
    decodeWithRequirements


class Hero:
    def __init__(self):
        self.currentHeroState = {}
        self.heroWeapon = {}
        self.heroPower = {}

    def createMegaMatrix(self, matrices):
        row1 = np.hstack((matrices[0:3]))
        row2 = np.hstack((matrices[3:6]))
        row3 = np.hstack((matrices[6:9]))
        full = np.concatenate((row1, row2, row3))
        full = np.pad(full, 1, mode='constant')
        return full

    def convert_matrix(self, matrix):
        matrix = np.reshape(matrix, (13,13))
        return matrix

    def encode_state(self, dictionaries):
        basicFeatures = np.zeros(169)
        weaponFeatures = np.zeros(169)
        basicFeatures[52:88] = [x for x in dictionaries[0].values()]
        weaponFeatures[88:91] = [x for x in dictionaries[1].values()]
        heroPowerFeatures = encode_complex_plane(dictionaries[2])
        basicAttr = self.convert_matrix(np.zeros(169))
        Battlecry_spell = self.convert_matrix(np.zeros(169))
        EoT = self.convert_matrix(np.zeros(169))
        SoT = self.convert_matrix(np.zeros(169))
        Deathrattle = self.convert_matrix(np.zeros(169))
        OnAttack = self.convert_matrix(np.zeros(169))
        OtherConditional = self.convert_matrix(np.zeros(169))
        filter1 = self.convert_matrix(np.zeros(169))
        filter2 = self.convert_matrix(np.zeros(169))

        basicFeatures = self.convert_matrix(basicFeatures)
        weaponFeatures = self.convert_matrix(weaponFeatures)
        heroPowerFeatures = self.convert_matrix(heroPowerFeatures)
        HeroPowerPlain = [basicAttr, heroPowerFeatures, EoT, SoT, Deathrattle, OnAttack, OtherConditional, filter1,
                          filter2]
        HeroPlain = [basicFeatures, Battlecry_spell, EoT, SoT, Deathrattle, OnAttack, OtherConditional, filter1,
                     filter2]
        WeaponPlain = [weaponFeatures, Battlecry_spell, EoT, SoT, Deathrattle, OnAttack, OtherConditional, filter1,
                       filter2]
        HERO_POWER = self.createMegaMatrix(HeroPowerPlain)
        HERO = self.createMegaMatrix(HeroPlain)
        WEAPON = self.createMegaMatrix(WeaponPlain)

        return HERO_POWER, HERO, WEAPON

    def HeroDecode(self, hero):
        #Basic hero features
        self.currentHeroState["health"] = hero.health
        self.currentHeroState["attack"] = hero.atk
        self.currentHeroState["base_health"] = 30
        self.currentHeroState["base_attack"] = 0
        self.currentHeroState["sleeping"] = 0 #ustawiam sobie na 0 bo wydaje mi sie ze bedzie wygodiej a nie zdarzy sie
        self.currentHeroState["frozen"] = int(hero.frozen)
        self.currentHeroState["charge"] = 0 #tez sie nie wydarzy
        self.currentHeroState["rush"] = int(hero.rush)
        self.currentHeroState["taunt"] = int(hero.taunt)
        self.currentHeroState["divineShield"] = 0 #tez sie nie wydarzy
        self.currentHeroState["isNoneType"] = 1 #CZY TO MA SENS?????
        self.currentHeroState["isMurloc"] = 0
        self.currentHeroState["isPirate"] = 0
        self.currentHeroState["isTotem"] = 0
        self.currentHeroState["isBeast"] = 0
        self.currentHeroState["isDemon"] = 0
        self.currentHeroState["isDragon"] = 0
        self.currentHeroState["isMech"] = 0
        self.currentHeroState["isElemental"] = 0
        self.currentHeroState["isBuffed"] = 1 if len(hero.buffs) else 0
        #currentHeroState["isBuffed"] = int(hero.powered_up) jedno albo drugie w sumie nie wiem
        self.currentHeroState["hasDeathrattle"] = 0
        self.currentHeroState["hasBattlecry"] = 0
        self.currentHeroState["hasAura"] = 0
        self.currentHeroState["spellDamage"] = 0
        self.currentHeroState["stealth"] = 0
        self.currentHeroState["isDamaged"] = int(hero.damaged)
        self.currentHeroState["windFury"] = hero.windfury
        self.currentHeroState["Position"] = 0
        self.currentHeroState["isImmune"] = int(hero.immune)
        self.currentHeroState["cantAttatck"] = int(hero.cant_attack)
        self.currentHeroState["cantAttatckHeroes"] = int(hero.cannot_attack_heroes)
        self.currentHeroState["cantBeTargetedSpellsHeroPowers"] = 1 if hero.cant_be_targeted_by_abilities == 1 and hero.cant_be_targeted_by_hero_powers == 1 else 0
        self.currentHeroState["isImmuneWhileAtk"] = int(hero.immune_while_attacking)
        self.currentHeroState["armor"] = hero.armor
        self.currentHeroState["canAttack"] = 0 if (hero.num_attacks == hero.max_attacks or hero.atk == 0) else 1 #jeszcze tu nie jestem tego pewny jak cos
        if hero.num_attacks == hero.max_attacks:
            self.currentHeroState["canAttack"] = 0
        else:
            self.currentHeroState["canAttack"] = 1
        if hero.atk == 0:
            self.currentHeroState["canAttack"] = 0
        self.currentHeroState["hasWeapon"] = 0 if hero.controller.weapon is None else 1

        #Basic equipped weapon features
        #self.heroWeapon["weaponId"] = 0 if hero.controller.weapon is None else hero.controller.weapon.data.card_id
        self.heroWeapon["weaponPoisonous"] = 0 if hero.controller.weapon is None else int(hero.controller.weapon.data.poisonous)
        self.heroWeapon["weaponAtt"] = 0 if hero.controller.weapon is None else hero.controller.weapon.data.atk
        self.heroWeapon["weaponDurability"] = 0 if hero.controller.weapon is None else hero.controller.weapon.data.durability
        #currentHeroState["weaponBuff"] = nie wiem co tu moze byc tbh


        #Hero Power features
        if str(hero) != "Thrall":
            for x in hero.power.data.scripts.activate:
                self.heroPower["AlwaysGet"] = 1
                getTargetedActionDetails(x, self.heroPower, hero)
        else:
            self.heroPower["AlwaysGet"] = 1
            self.heroPower["SetAmountSummon"] = 1
            self.heroPower["Summon"] = 1
            self.heroPower["SummonTimes"] = 1
            self.heroPower["SummonTagets"] = 75497472

            self.heroPower["SummonFromEntourage"] = 1
            sum_health = 0
            sum_atk = 0
            sum_cost = 0
            for y in hero.power.data.scripts.entourage:
                card = Card(y)
                sum_atk += card.atk
                sum_health += card.health
                sum_cost += card.cost
            self.heroPower["SummonedAvgHealth"] = sum_health / len(hero.power.data.scripts.entourage)
            self.heroPower["SummonedAvgAttack"] = sum_atk / len(hero.power.data.scripts.entourage)
            self.heroPower["SummonedAvgCost"] = sum_cost / len(hero.power.data.scripts.entourage)
            self.heroPower["SummonedCalculatedValue"] = 1
            self.heroPower["AlwaysGetSummmon"] = 1
        return self.currentHeroState, self.heroWeapon, self.heroPower