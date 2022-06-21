import operator

import fireplace
from fireplace.actions import SetTag, Silence, Heal, Hit, Destroy, GainArmor, Draw, Discard, Summon, Bounce
from fireplace.card import Card
from fireplace.dsl import LazyValue, RandomEntourage
from hearthstone.enums import Race, GameTag, PlayReq


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
                "taunt": int(card.taunt),
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
    if len(card.requirements) != 0:
        for x in card.data.scripts.requirements:
            if type(x) is PlayReq:
                currentBattlecryEffect["AlwaysGet"] = 0
                break
    for x in card.data.scripts.play:
        # if isinstance(x, fireplace.actions.Buff) or (
        #        isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if, fireplace.actions.Buff)):
        #    getBuffDetails(x, currentBattlecryEffect, card)
        if isinstance(x, fireplace.actions.TargetedAction) or (
                isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if, fireplace.actions.TargetedAction)):
            getTargetedActionDetails(x, currentBattlecryEffect, card)
        #if isinstance(x, fireplace.actions.TargetedAction) or (
        #        isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if, fireplace.actions.TargetedAction)):
        #    getTargetedActionDetails(x, currentBattlecryEffect, card)
    return currentBattlecryEffect

    # TODO


def getTargetedActionDetails(x, currentBattlecryEffect, card):
    if "AlwaysGet" not in currentBattlecryEffect:
        if isinstance(x, fireplace.dsl.evaluator.Find):
            currentBattlecryEffect["AlwaysGet"] = 0
            if x._if is None:
                x = x._else
            else:
                x = x._if
        else:
            currentBattlecryEffect["AlwaysGet"] = 1
    if isinstance(x, fireplace.dsl.evaluator.Dead):
        selector = x.selector
    elif isinstance(x, fireplace.dsl.LazyNumEvaluator):
        selector = x.num.selector
    else:
        selector = x.get_args(card)[0]
    times = 0
    if hasattr(x, "times"):
        times = getTimes(x, card, currentBattlecryEffect)
    # targets = x.get_targets(card, selector)
    # if isinstance(selector, fireplace.dsl.selector.FuncSelector) and len(targets) == 1 and targets[0] == card:
    #    currentBattlecryEffect["CanAffectSelf"] = 1
    # elif isinstance(selector, fireplace.dsl.selector.FuncSelector) and targets[0] is None:
    #    currentBattlecryEffect["IChooseCard"] = 1
    # else:

    if isinstance(x, fireplace.actions.Buff):
        currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        getBuffDetails(x, currentBattlecryEffect, card, times)
    elif isinstance(x, SetTag):
        if GameTag.DIVINE_SHIELD in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
            currentBattlecryEffect["GiveDivShield"] = 1
        elif GameTag.TAUNT in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
            currentBattlecryEffect["GiveTaunt"] = 1
        elif GameTag.STEALTH in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
            currentBattlecryEffect["GiveStealth"] = 1
        elif GameTag.POISONOUS in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
            currentBattlecryEffect["GivePoison"] = 1
        elif GameTag.FROZEN in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
            currentBattlecryEffect["Freeze"] = 1
    elif isinstance(x, Silence):
        currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["GiveSilence"] = 1
    elif isinstance(x, Heal):
        currentBattlecryEffect["HealTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["HealAmount"] = getAmount(x, card, currentBattlecryEffect)
    elif isinstance(x, Hit):
        currentBattlecryEffect["HitTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["HitAmount"] = getAmount(x, card, currentBattlecryEffect)
    elif isinstance(x, Destroy):
        currentBattlecryEffect["DestroyTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["Destroy"] = 1
    elif isinstance(x, GainArmor):
        currentBattlecryEffect["GainArmorTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["GainArmorAmount"] = getAmount(x, card, currentBattlecryEffect)
    elif isinstance(x, Draw):
        currentBattlecryEffect["DrawCardsTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["DrawCards"] = 1
    elif isinstance(x, Discard):
        currentBattlecryEffect["DiscardTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["DiscardCards"] = 1
    elif isinstance(x, Summon):
        getSummonDetails(x, card, currentBattlecryEffect)
    elif isinstance(x, Bounce):
        currentBattlecryEffect["BounceTargets"] = decodeTarget(selector)
        currentBattlecryEffect["BounceCards"] = 1
    if selector is not None:
        decodeResultStr(decodeWithRequirements(decodeTarget(selector), card.data.requirements))

def getSummonDetails(x, card, currentEffect):
    selector = x.get_args(card)[0]
    currentEffect["Summon"] = 1
    currentEffect["SummonTagets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
    toSummon = Card(x.get_args(card)[1])
    currentEffect["SummonedHealth"] = toSummon.health
    currentEffect["SummonedAttack"] = toSummon.atk
    currentEffect["SummonedCost"] = toSummon.cost
    currentEffect["SummonTagets"] = decodeTarget(selector)
    toSummonID = x.get_args(card)[1]
    if type(toSummonID) is RandomEntourage:
        #TODO hmmm
        currentEffect["FromEntourage"] = 1
    else:
        toSummon = Card(toSummonID)
        currentEffect["SummonedHealth"] = toSummon.health
        currentEffect["SummonedAttack"] = toSummon.atk
        currentEffect["SummonedCost"] = toSummon.cost

def getAmount(x, card, currEffect):
    if type(x.get_args(card)[-1]) is not int:
        print("DEPENDANT SOMETHING FOUND!!!")
        currEffect["SetAmount"] = 0
        return x.get_args(card)[-1].evaluate(card)
    else:
        currEffect["SetAmount"] = 1
        return x.get_args(card)[-1]

def getTimes(x, card, currEffect):
    times = x.times
    if isinstance(times, LazyValue):
        times = times.evaluate(card)
        currEffect["SetAmount"] = 0
    else:
        currEffect["SetAmount"] = 1
    return times


def getBuffDetails(x, currEffect, card, times):
    if x._kwargs != {}:
        currEffect["SetAmount"] = 0
    buff = x.get_target_args(card, card)[0]
    if hasattr(buff.data.scripts, "apply"):
        currEffect["setsAttackToHealth"] = 1
    # hard coding- only inner fire has this
    if hasattr(buff.data.scripts, "max_health"):
        pass
    if currEffect.get("setsAttackToHealth") is None:
        currEffect["AttackValue"] = buff.atk * times
        currEffect["HealthValue"] = buff.max_health * times
        if hasattr(buff.data.scripts, "atk") or hasattr(buff.data.scripts,
                                                        "max_health") or "max_health" in x._kwargs:
            currEffect["AddValue"] = 0
            if (hasattr(buff.data.scripts, "atk") and buff.data.scripts.atk(0, 10) == buff.atk) or (
                    hasattr(buff.data.scripts, "max_health") and buff.data.scripts.max_health(0,
                                                                                              10) == buff.max_health):
                currEffect["SetValue"] = 1
                currEffect["MultiplyValue"] = 0
            else:
                currEffect["SetValue"] = 0
                currEffect["MultiplyValue"] = 1
                if hasattr(buff.data.scripts, "atk"):
                    currEffect["AttackValue"] = buff.data.scripts.atk(0, 1)
                if hasattr(buff.data.scripts, "max_health"):
                    currEffect["HealthValue"] = buff.data.scripts.max_health(0, 1)
                # hard coding divine spirit
                if "max_health" in x._kwargs:
                    currEffect["selfHealthValue"] = 2

        else:
            currEffect["AddValue"] = 1
            currEffect["SetValue"] = 0
            currEffect["MultiplyValue"] = 0
        currEffect["Permanent"] = 1 if int(buff.one_turn_effect) == 0 else 0
    else:
        currEffect["Permanent"] = 1
        currEffect["AddValue"] = 1

def decodeWithRequirements(result, requirements):
    if PlayReq.REQ_MINION_TARGET in requirements:
        result = result & (~(1<<21))
    if PlayReq.REQ_HERO_TARGET in requirements:
        result = result & (~(1<<22))
    if PlayReq.REQ_FRIENDLY_TARGET in requirements:
        result = result & (~(1<<24))
    if PlayReq.REQ_ENEMY_TARGET in requirements:
        result = result & (~(1<<23)) & (~(1<<25))
    return result

def decodeFuncSelector(func):
    if func == fireplace.dsl.selector.SELF:
        return 1 << 25
    if func == fireplace.dsl.selector.TARGET:
        return 0b111111 << 20
    if func == fireplace.dsl.selector.OTHER_CLASS_CHARACTER:
        return ~0
    if func == fireplace.dsl.selector.FRIENDLY_CLASS_CHARACTER:
        return ~0
    if func == fireplace.dsl.selector.LEFTMOST_HAND:
        return ~0
    if func == fireplace.dsl.selector.RIGTHMOST_HAND:
        return ~0
    if func == fireplace.dsl.selector.OWNER:
        return ~0
    if func == fireplace.dsl.selector.ATTACK_TARGET:
        return ~0
    return 0

def decodeOp(left, op, right):
    if op == operator.or_:
        return left | right
    if op == operator.add:
        return "?+?" #tu chce wyjatek bo tego chyba nie bedzie
    if op == operator.and_:
        return left & right
    if op == operator.sub:
        return left & (~right)
    if op == operator.eq:
        return left | right # nie wiem w sumie
    if op == operator.le:
        return left | right # nie wiem w sumie
    return ">O<"

def decodeEnum(enum):
    if isinstance(enum, str):
        return 0
    if enum == fireplace.dsl.selector.Zone.PLAY:
        return ~0
    if enum == fireplace.dsl.selector.CardType.MINION:
        return 1 << 22 | 1 << 23 | 1 << 24 | 1 << 25 | 1 << 26# czy na self mogę zagra
    if enum == fireplace.dsl.selector.CardType.HERO: #na hero sie gra np leczenie/buffa
        return 1 << 21 | 1 << 23 | 1 << 24 | 1 << 26
    if enum == fireplace.dsl.selector.CardType.PLAYER: #na gracza sie gra np przyzwanie(przyzwij minionka)
        return (1 << 23) | (1 << 24) | 1 << 26#aktywuję self i enemy aby pozniej kontroler mogl cos wylaczyc
    if enum == fireplace.dsl.selector.GameTag.CONTROLLER:
        return 0
    if enum == fireplace.dsl.selector.GameTag.DORMANT:
        return 0
    if enum == fireplace.dsl.selector.GameTag.DAMAGE:
        return (1 << 26)
    if enum == fireplace.dsl.selector.GameTag.SECRET:
        return (0b11 << 23)
    if enum == fireplace.dsl.selector.Zone.SECRET:
        return (0b11 << 23)
    return (1 << 26)

def decodeController(controller):
    if isinstance(controller, fireplace.dsl.selector.Opponent):
        return ~(1 << 23) & ~(1 << 25)
    else:
        return ~(1 << 24)

def decodeBoardPosition(direction):
    if direction == fireplace.dsl.selector.BoardPositionSelector.Direction.LEFT:
        return 1 << 28
    elif direction == fireplace.dsl.selector.BoardPositionSelector.Direction.RIGHT:
        return 1 << 27
    else:
        return " >D<"

# 1 << 31 oznacza random
# ostatnie 4 bity(czyli max. 16) oznaczają 'times' czyli ile celów losuje
# jeśli target.times będzie >=16 to mam nadzieję że tak nie będzie bo się spowrotem wyzeruje
def decodeTarget(target):
    if target is None:
        return 0 #unknown value(co to znaczy w ogóle ze target is none)
    if isinstance(target, fireplace.dsl.selector.RandomSelector):
        return (1 << 31)+decodeTarget(target.child)+(target.times%16)

    if isinstance(target, fireplace.dsl.selector.SetOpSelector):
        return decodeOp(decodeTarget(target.left), target.op, decodeTarget(target.right))

    if isinstance(target, fireplace.dsl.selector.EnumSelector):
        return decodeEnum(target.tag_enum)

    if isinstance(target, fireplace.dsl.selector.ComparisonSelector):
        return decodeOp(decodeTarget(target.left), target.op, decodeTarget(target.right))

    if isinstance(target, fireplace.dsl.selector.AttrValue):
        return decodeEnum(target.tag)
    if isinstance(target, fireplace.dsl.selector.Controller):
        return decodeController(target)
    if isinstance(target, fireplace.dsl.selector.FuncSelector) | isinstance(target, fireplace.dsl.selector.FilterSelector):
        return decodeFuncSelector(target)
    if isinstance(target, int):
        return 0
    if isinstance(target, fireplace.dsl.selector.BoardPositionSelector):
        return decodeBoardPosition(target.direction)
    return " Unknown " #wyjatek i dobrze

def decodeResultStr(result):
    if result & 1 << 31:
        print("Random tyle razy: "+str(result&0b1111))
    if result & 1 << 28:
        print("Lewo")
    if result & 1 << 27:
        print("Prawo")
    if result & 1 << 26:
        print("Nie jest conditionalem")
    if result & 1 << 25:
        print("Na siebie")
    if result & 1 << 24:
        print("Na enemy")
    if result & 1 << 23:
        print("Na ally")
    if result & 1 << 22:
        print("Miniony")
    if result & 1 << 21:
        print("Na boha")



def mapEndOfTurn(card):
    endOfTurnEffect = {}
    if len(card.requirements) != 0:
        for x in card.data.scripts.requirements:
            if type(x) is PlayReq:
                endOfTurnEffect["AlwaysGet"] = 0
                break
    for x in card.data.scripts.events:
        for y in x.actions:
            getTargetedActionDetails(y, endOfTurnEffect, card)
    print(card.data.strings[GameTag.CARDNAME]['enUS']+"  "+str(endOfTurnEffect))
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

    # snowchugger
    # cutpurse ale nie ma go chyba w kartach
    # alley armorsmith
    for x in card.data.scripts.enrage:
        getTargetedActionDetails(x, onAttackEffect, card)
    # loop for detecting what combo does
    for x in card.data.scripts.combo:
        #effect = card.get_actions("combo")[0].get_target_args(card, card)[0]
        onAttackEffect["AlwaysGet"] = 0
        if isinstance(x, fireplace.actions.TargetedAction) or (
                isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if,
                                                                            fireplace.actions.TargetedAction)):

            getTargetedActionDetails(x, onAttackEffect, card)

    for x in card.data.scripts.deathrattle:
        onAttackEffect["AlwaysGet"] = 1
        if isinstance(x, fireplace.actions.TargetedAction) or (
                isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if,
                                                                            fireplace.actions.TargetedAction)):
            getTargetedActionDetails(x, onAttackEffect, card)


    for x in card.data.scripts.events:
        if isinstance(x, fireplace.actions.EventListener):
            if isinstance(x.trigger, fireplace.actions.Damage):
                if isinstance(x, fireplace.actions.TargetedAction) or (
                        isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if,
                                                                                   fireplace.actions.TargetedAction)):
                    getTargetedActionDetails(x, onAttackEffect, card)
                #print("On attack effect (event Damage)")
    return onAttackEffect
