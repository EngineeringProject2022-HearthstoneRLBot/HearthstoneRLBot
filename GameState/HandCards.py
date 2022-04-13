import fireplace
from fireplace.dsl import LazyValue


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
            "isNoneType": 1 if card.race == 1 else 0,
            "isMurloc": 1 if card.race == 14 else 0,
            "isPirate": 1 if card.race == 23 else 0,
            "isTotem": 1 if card.race == 21 else 0,
            "isBeast": 1 if card.race == 20 else 0,
            "isDemon": 1 if card.race == 15 else 0,
            "isDragon": 1 if card.race == 24 else 0,
            "isMech": 1 if card.race == 17 else 0,
            "isElemental": 1 if card.race == 18 else 0,
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
        self.battlecrySpellEffectPlane = {}
        self.endOfTurnEffectPlane = {}
        self.startOfTurnEffectPlane = {}
        self.conditionalEffectPlane = {}
        self.onAttackPlane = {}

    # to serve as template for extracting more complext features
    def mapToInput(self):
        for x in self.play:
            if isinstance(x, fireplace.actions.Buff):
                selector = x.get_args(self.card)[0]
                times = x.times
                if isinstance(times, LazyValue):
                    times = times.evaluate(self.card)
                if self.card in x.get_targets(self.card, selector):
                    buff = x.get_target_args(self.card, self.card)[0]
                    value = buff.max_health * times
