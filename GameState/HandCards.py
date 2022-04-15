import fireplace
from fireplace.dsl import LazyValue
from hearthstone.enums import Race


class HandCard:

    def __init__(self, card):
        self.handCardFeatures = {
            "cost": card.cost,
            "poweredUp": int(card.powered_up),
            "isMinion": 1 if card.type == 4 else 0,
            "isSpell": 1 if card.type == 5 else 0,
            "isWeapon": 1 if card.type == 7 else 0,
            "currDiscount": card.data.cost - card.cost
        }
        self.minionFeatures = {}
        if self.handCardFeatures["isMinion"]:
            self.minionFeatures = {
                "currentHealth": card.health,
                "currentAttack": card.atk,
                "baseHealth": card.data.health,
                "baseAtt": card.data.atk,
                "sleeping": int(card.asleep),
                "frozen": int(card.frozen),
                "charge": int(card.charge),
                "rush": int(card.rush),
                "taunt": int(card.rush),
                "divineShield": int(card.divine_shield),
                "isNoneType": 1 if card.race == Race.INVALID else 0,
                "isMurloc": 1 if card.race == Race.MURLOC else 0,
                "isPirate": 1 if card.race == Race.PIRATE else 0,
                "isTotem": 1 if card.race == Race.TOTEM else 0,
                "isBeast": 1 if card.race == Race.BEAST else 0,
                "isDemon": 1 if card.race == Race.DEMON else 0,
                "isDragon": 1 if card.race == Race.DRAGON else 0,
                "isMech": 1 if card.race == Race.MECHANICAL else 0,
                "isElemental": 1 if card.race == Race.ELEMENTAL else 0,
                "isBuffed": 1 if len(card.buffs) != 0 else 0,
                "hasDeathrattle": 1 if len(card.deathrattles) != 0 else 0,
                "hasBattlecry": int(card.has_battlecry),
                "hasAura": int(card.aura),
                "hasCondEff": 0,  # tricky one
                "hasEoTEff": 0,  # tricky one
                "hasSoTEff": 0,  # tricky one
                "spellDamage": card.spellpower,
                "stealth": int(card.stealthed),
                "isDamaged": int(card.damaged),
                "windfury": card.windfury,
                "position": card.zone_position,  # probably to be ommitted
                "isImmune": int(card.immune),
                "cantAttack": int(card.cant_attack),
                "cantAttackHeroes": int(card.cannot_attack_heroes),
                "cantBeTargetedSpellsHeroPowers": 1 if card.cant_be_targeted_by_abilities == 1 and card.cant_be_targeted_by_hero_powers == 1 else 0,
                "cleave": 0}
        self.battlecrySpellEffectPlane, self.endOfTurnEffectPlane, self.startOfTurnEffectPlane, self.conditionalEffectPlane, self.onAttackPlane = self.mapComplexFeatures(card)

    # to serve as template for extracting more complext features
    def mapComplexFeatures(self,card):
        battlecrySpellEffectPlane = {}
        endOfTurnEffectPlane = {}
        startOfTurnEffectPlane = {}
        conditionalEffectPlane = {}
        onAttackPlane = {}

        for x in card.data.scripts.play:
            currentBattlecryEffect = {}
            if isinstance(x, fireplace.actions.Buff) or (isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if,fireplace.actions.Buff)):
                if isinstance(x, fireplace.actions.Buff):
                    currentBattlecryEffect["AlwaysGet"] = 1
                else:
                    currentBattlecryEffect["AlwaysGet"] = 0
                    x = x._if
                selector = x.get_args(card)[0]
                targets = x.get_targets(card, selector)
                if isinstance(selector, fireplace.dsl.selector.FuncSelector) and len(targets) == 1 and targets[0] == card:
                    selfFlag = True
                times = x.times
                if isinstance(times, LazyValue):
                    times = times.evaluate(card)
                    currentBattlecryEffect["SetAmount"] = 0
                else:
                    currentBattlecryEffect["SetAmount"] = 1
                if x._kwargs != {}:
                    currentBattlecryEffect["SetAmount"] = 0
                buff = x.get_target_args(card, card)[0]
                currentBattlecryEffect["Permanent"] = int(buff.one_turn_effect)
                currentBattlecryEffect["selfHealthValue"] = buff.max_health * times
                currentBattlecryEffect["selfAttackValue"] = buff.atk * times
        return battlecrySpellEffectPlane, endOfTurnEffectPlane, startOfTurnEffectPlane, conditionalEffectPlane, onAttackPlane