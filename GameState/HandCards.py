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
        self.battlecrySpellEffectPlane, self.endOfTurnEffectPlane, self.startOfTurnEffectPlane, self.conditionalEffectPlane, self.onAttackPlane = self.mapComplexFeatures(
            card)

    # to serve as template for extracting more complex features
    def mapComplexFeatures(self, card):
        battlecrySpellEffectPlane = mapBattlecrySpells(card)
        endOfTurnEffectPlane = mapEndOfTurn(card)
        startOfTurnEffectPlane = mapStartOfTurn(card)
        conditionalEffectPlane = mapConditional(card)
        onAttackPlane = mapOnAttack(card)

        # buff.data.scripts.atk!!!
        return battlecrySpellEffectPlane, endOfTurnEffectPlane, startOfTurnEffectPlane, conditionalEffectPlane, onAttackPlane


def mapBattlecrySpells(card):
    currentBattlecryEffect = {}
    for x in card.data.scripts.play:
        if isinstance(x, fireplace.actions.Buff) or (
                isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if, fireplace.actions.Buff)):
            if isinstance(x, fireplace.actions.Buff):
                currentBattlecryEffect["AlwaysGet"] = 1
            else:
                currentBattlecryEffect["AlwaysGet"] = 0
                x = x._if
            selector = x.get_args(card)[0]
            targets = x.get_targets(card, selector)
            if isinstance(selector, fireplace.dsl.selector.FuncSelector) and len(targets) == 1 and targets[
                0] == card:
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
            if hasattr(buff.data.scripts, "apply"):
                currentBattlecryEffect["setsAttackToHealth"] = 1
            # hard coding- only inner fire has this
            if hasattr(buff.data.scripts, "max_health"):
                pass
            if currentBattlecryEffect.get("setsAttackToHealth") is None:
                currentBattlecryEffect["selfAttackValue"] = buff.atk * times
                currentBattlecryEffect["selfHealthValue"] = buff.max_health * times
                if hasattr(buff.data.scripts, "atk") or hasattr(buff.data.scripts,
                                                                "max_health") or "max_health" in x._kwargs:
                    currentBattlecryEffect["AddValue"] = 0
                    if (hasattr(buff.data.scripts, "atk") and buff.data.scripts.atk(0, 10) == buff.atk) or (
                            hasattr(buff.data.scripts, "max_health") and buff.data.scripts.max_health(0,
                                                                                                      10) == buff.max_health):
                        currentBattlecryEffect["SetValue"] = 1
                        currentBattlecryEffect["MultiplyValue"] = 0
                    else:
                        currentBattlecryEffect["SetValue"] = 0
                        currentBattlecryEffect["MultiplyValue"] = 1
                        if hasattr(buff.data.scripts, "atk"):
                            currentBattlecryEffect["selfAttackValue"] = buff.data.scripts.atk(0, 1)
                        if hasattr(buff.data.scripts, "max_health"):
                            currentBattlecryEffect["selfHealthValue"] = buff.data.scripts.max_health(0, 1)
                        # hard coding divine spirit
                        if "max_health" in x._kwargs:
                            currentBattlecryEffect["selfHealthValue"] = 2

                else:
                    currentBattlecryEffect["AddValue"] = 1
                    currentBattlecryEffect["SetValue"] = 0
                    currentBattlecryEffect["MultiplyValue"] = 0
                currentBattlecryEffect["Permanent"] = int(buff.one_turn_effect)
            else:
                currentBattlecryEffect["Permanent"] = 1
                currentBattlecryEffect["AddValue"] = 1
    return currentBattlecryEffect

    # TODO


def mapEndOfTurn(card):
    endOfTurnEffect = {}
    return endOfTurnEffect

    # TODO


def mapConditional(card):
    conditionalEffect = {}
    return conditionalEffect

    # TODO


def mapStartOfTurn(card):
    startOfTurnEffect = {}
    return startOfTurnEffect

    # TODO

def mapOnAttack(card):
    comboEffect = {}
    inspireEffect = {}
    onAttackEffect = {}

    for x in card.data.scripts.inspire:
        effect = card.get_actions("combo")[0].get_target_args(card, card)[0]
        #tu mozna inspire dorzucic ewentualnie czy cos..

    #loop for detecting what combo does
    for x in card.data.scripts.combo:
        effect = card.get_actions("combo")[0].get_target_args(card, card)[0]
        comboEffect["AlwaysGet"] = 0
        if isinstance(x, fireplace.actions.Hit):
            print("Combo that simply does damage")

        if isinstance(x, fireplace.actions.Buff):
            print("Combo that buffs")
            #86
            #87 patrzysz czy x times czy lazy value
            #94 linijka refer to buff
            selector = x.get_args(card)[0]
            targets = x.get_targets(card, selector)
            if isinstance(selector, fireplace.dsl.selector.FuncSelector) and len(targets) == 1 and targets[0] == card:
                selfFlag = True
            times = x.times
            if isinstance(times, LazyValue):
                times = times.evaluate(card)
                print("Number of times trigger: ", times)
                comboEffect["SetAmount"] = 0
            else:
                comboEffect["SetAmount"] = 1
            comboEffect["selfAttackValue"] = effect.atk * times
            comboEffect["selfHealthValue"] = effect.max_health * times

            if hasattr(effect.data.scripts, "atk") or hasattr(effect.data.scripts,"max_health"):
                    comboEffect["AddValue"] = 0
                    if (hasattr(effect.data.scripts, "atk") and effect.data.scripts.atk(0, 10) == effect.atk) or (
                                hasattr(effect.data.scripts, "max_health") and effect.data.scripts.max_health(0,10) == effect.max_health):
                            comboEffect["SetValue"] = 1
                            comboEffect["MultiplyValue"] = 0
                    else:
                        comboEffect["SetValue"] = 0
                        comboEffect["MultiplyValue"] = 1
                        if hasattr(effect.data.scripts, "atk"):
                            comboEffect["selfAttackValue"] = comboEffect.data.scripts.atk(0, 1)
                        if hasattr(effect.data.scripts, "max_health"):
                            comboEffect["selfHealthValue"] = effect.data.scripts.max_health(0, 1)
            else:
                comboEffect["AddValue"] = 1
                comboEffect["SetValue"] = 0
                comboEffect["MultiplyValue"] = 0
            comboEffect["Permanent"] = int(effect.one_turn_effect)
        #else:
         #       comboEffect["Permanent"] = 1
          #      comboEffect["AddValue"] = 1







        #przy summonie nalezy rozpracowac selector, bo sa karty ktore summonuja dla przeciwnika!!!
        if isinstance(x, fireplace.actions.Summon):
            selector = x.get_args(card)[0]
            targets = x.get_targets(card, selector)
            print("Combo that summons a: "
                  + str(effect[0].atk) + " " + str(effect[0].health) + " minion of cost: " + str(effect[0].cost))

    for x in card.data.scripts.events:
        if isinstance(x, fireplace.actions.EventListener):
            if isinstance(x.trigger, fireplace.actions.Damage):
                print("On attack effect (event Damage)")
    return onAttackEffect
