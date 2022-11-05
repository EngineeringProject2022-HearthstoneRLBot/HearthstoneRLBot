from hearthstone.enums import Race, GameTag
import numpy as np

from GameState.StateEncoder import encode_complex_plane, mapBattlecrySpells, mapEndOfTurn, mapConditional, \
    mapStartOfTurn, mapOnAttack, mapDeathrattle

DEBUG = False

class HandCard:

    def __init__(self, card):
        # for debugging matrix encoding
        self.card = card
        self.handCardFeatures = {
            "cost": card.cost,
            "poweredUp": int(card.powered_up),
            "isMinion": 1 if card.type == 4 else 0,
            "isSpell": 1 if card.type == 5 else 0,
            "isWeapon": 1 if card.type == 7 else 0,
            "currDiscount": card.data.cost - card.cost
        }
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
                "taunt": int(card.taunt),
                "divineShield": int(card.divine_shield),
                "isNoneType": 1 if card.race == Race.INVALID else 0,
                "isMurloc": 1 if (card.race == Race.MURLOC or card.race == Race.ALL) else 0,
                "isPirate": 1 if (card.race == Race.PIRATE or card.race == Race.ALL) else 0,
                "isTotem": 1 if (card.race == Race.TOTEM or card.race == Race.ALL) else 0,
                "isBeast": 1 if (card.race == Race.BEAST or card.race == Race.ALL) else 0,
                "isDemon": 1 if (card.race == Race.DEMON or card.race == Race.ALL) else 0,
                "isDragon": 1 if (card.race == Race.DRAGON or card.race == Race.ALL) else 0,
                "isMech": 1 if (card.race == Race.MECHANICAL or card.race == Race.ALL) else 0,
                "isElemental": 1 if (card.race == Race.ELEMENTAL or card.race == Race.ALL) else 0,
                "isBuffed": 1 if len(card.buffs) != 0 else 0,
                "hasDeathrattle": 1 if len(card.deathrattles) != 0 else 0,
                "hasBattlecry": int(card.has_battlecry),
                "hasAura": int(card.aura),
                "spellDamage": card.spellpower,
                "stealth": int(card.stealthed),
                "isDamaged": int(card.damaged),
                "windfury": card.windfury,
                "position": card.zone_position,  # probably to be ommitted
                "isImmune": int(card.immune),
                "cantAttack": int(card.cant_attack),
                "cantAttackHeroes": int(card.cannot_attack_heroes),
                "cantBeTargetedSpellsHeroPowers": 1 if card.cant_be_targeted_by_abilities == 1 and card.cant_be_targeted_by_hero_powers == 1 else 0,
                "exhausted": 1 if card.exhausted else 0
            }
        elif self.handCardFeatures["isWeapon"]:
            self.weaponFeatures = {
                "currentdurability": card.durability,
                "currentAttack": card.atk,
                "baseDurability": card.max_durability}
        self.battlecrySpellEffectPlane, self.endOfTurnEffectPlane, self.startOfTurnEffectPlane, self.conditionalEffectPlane, self.onAttackPlane, self.deathrattleEffectPlane = self.mapComplexFeatures(
            card)

    @staticmethod
    def convert_matrix(matrix):
        matrix = np.reshape(matrix, (13, 13))
        # matrix = np.pad(matrix, 1, mode='constant')
        return matrix

    @staticmethod
    def merge_matrices(matrices):
        row1 = np.hstack((matrices[0:3]))
        row2 = np.hstack((matrices[3:6]))
        row3 = np.hstack((matrices[6:9]))
        full = np.concatenate((row1, row2, row3))
        #full = np.pad(full, 1, mode='constant')
        #full = np.delete(full, 0, 1)
        return full

    def encode_state(self, debug=False):
        basicFeatures = np.zeros(169)
        basicFeatures[0:6] = [x for x in self.handCardFeatures.values()]
        if self.handCardFeatures["isMinion"] == 1:
            basicFeatures[51:84] = [x for x in self.minionFeatures.values()]
        elif self.handCardFeatures["isWeapon"] == 1:
            basicFeatures[51:54] = [x for x in self.weaponFeatures.values()]

        BattlecrySpell = encode_complex_plane(self.battlecrySpellEffectPlane)
        EoT = encode_complex_plane(self.endOfTurnEffectPlane)
        SoT = encode_complex_plane(self.startOfTurnEffectPlane)
        Deathrattle = encode_complex_plane(self.deathrattleEffectPlane)
        OnAttack = encode_complex_plane(self.onAttackPlane)
        OtherConditional = encode_complex_plane(self.conditionalEffectPlane)
        if debug:
            return [basicFeatures, BattlecrySpell, EoT, SoT, Deathrattle, OnAttack, OtherConditional]

        basicFeatures = HandCard.convert_matrix(basicFeatures)
        BattlecrySpell = HandCard.convert_matrix(BattlecrySpell)
        EoT = HandCard.convert_matrix(EoT)
        SoT = HandCard.convert_matrix(SoT)
        Deathrattle = HandCard.convert_matrix(Deathrattle)
        OnAttack = HandCard.convert_matrix(OnAttack)
        OtherConditional = HandCard.convert_matrix(OtherConditional)
        filter1 = HandCard.convert_matrix(np.zeros(169))
        filter2 = HandCard.convert_matrix(np.zeros(169))

        matrices = [basicFeatures, BattlecrySpell, EoT, SoT, Deathrattle, OnAttack, OtherConditional, filter1, filter2]
        matrix = HandCard.merge_matrices(matrices)
        return matrix



    # to serve as template for extracting more complex features
    def mapComplexFeatures(self, card):
        if card.data.strings[GameTag.CARDNAME]['enUS'] == "Arcane Missiles":
            # use as a breakpoint for catching a specific card in the list
            asda = 33
        battlecrySpellEffectPlane = mapBattlecrySpells(card)
        endOfTurnEffectPlane = mapEndOfTurn(card)
        startOfTurnEffectPlane = mapStartOfTurn(card)
        conditionalEffectPlane = mapConditional(card)
        onAttackPlane = mapOnAttack(card)
        deathrattleEffectPlane = mapDeathrattle(card)

        # print("BTC " + card.data.strings[GameTag.CARDNAME]['enUS'] + "  " + str(battlecrySpellEffectPlane))
        # print("EOT " + card.data.strings[GameTag.CARDNAME]['enUS'] + "  " + str(endOfTurnEffectPlane))
        # print("SOT " + card.data.strings[GameTag.CARDNAME]['enUS'] + "  " + str(startOfTurnEffectPlane))
        # print("CON " + card.data.strings[GameTag.CARDNAME]['enUS'] + "  " + str(conditionalEffectPlane))
        # print("ONA " + card.data.strings[GameTag.CARDNAME]['enUS'] + "  " + str(onAttackPlane))
        # print("DR " + card.data.strings[GameTag.CARDNAME]['enUS'] + "  " + str(deathrattleEffectPlane))
        # buff.data.scripts.atk!!!
        return battlecrySpellEffectPlane, endOfTurnEffectPlane, startOfTurnEffectPlane, conditionalEffectPlane, onAttackPlane, deathrattleEffectPlane


