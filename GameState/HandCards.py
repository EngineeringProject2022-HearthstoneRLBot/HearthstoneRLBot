
import operator

import fireplace
from fireplace.actions import SetTag, Silence, Heal, Hit, Destroy
from fireplace.dsl import LazyValue
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
        if isinstance(x, fireplace.actions.Buff) or (
                isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if, fireplace.actions.Buff)):
            getBuffDetails(x, currentBattlecryEffect, card)
        if isinstance(x, fireplace.actions.TargetedAction) or (
                isinstance(x, fireplace.dsl.evaluator.Find) and isinstance(x._if, fireplace.actions.TargetedAction)):
            getTargetedActionDetails(x, currentBattlecryEffect, card)
    return currentBattlecryEffect

    # TODO

def getTargetedActionDetails(x, currentBattlecryEffect, card):
    if "AlwaysGet" not in currentBattlecryEffect:
        if isinstance(x, fireplace.dsl.evaluator.Find):
            currentBattlecryEffect["AlwaysGet"] = 0
        else:
            currentBattlecryEffect["AlwaysGet"] = 1
    if isinstance(x, fireplace.dsl.evaluator.Find):
        x = x._if
    selector = x.get_args(card)[0]
    targets = x.get_targets(card, selector)
    if isinstance(selector, fireplace.dsl.selector.FuncSelector) and len(targets) == 1 and targets[0] == card:
        currentBattlecryEffect["CanAffectSelf"] = 1
    elif isinstance(selector, fireplace.dsl.selector.FuncSelector) and targets[0] is None:
        currentBattlecryEffect["IChooseCard"] = 1
    if isinstance(x, SetTag):
        if GameTag.DIVINE_SHIELD in x._args[1]:
            currentBattlecryEffect["GiveDivShield"] = 1
        if GameTag.TAUNT in x._args[1]:
            currentBattlecryEffect["GiveTaunt"] = 1
        if GameTag.STEALTH in x._args[1]:
            currentBattlecryEffect["GiveStealth"] = 1
        if GameTag.POISONOUS in x._args[1]:
            currentBattlecryEffect["GivePoison"] = 1
        if GameTag.FROZEN in x._args[1]:
            currentBattlecryEffect["Freeze"] = 1
    if isinstance(x, Silence):
        currentBattlecryEffect["GiveSilence"] = 1
    if isinstance(x, Heal):
        currentBattlecryEffect["HealAmount"] = x.get_args(card)[1]
    if isinstance(x, Hit):
        currentBattlecryEffect["HitAmount"] = x.get_args(card)[1]
    if isinstance(x, Destroy):
        currentBattlecryEffect["Destroy"] = 1


def getBuffDetails(x, currEffect, card):
    if "AlwaysGet" not in currEffect:
        if isinstance(x, fireplace.actions.Buff):
            currEffect["AlwaysGet"] = 1
        else:
            currEffect["AlwaysGet"] = 0
            x = x._if
    if isinstance(x, fireplace.dsl.evaluator.Find):
        x = x._if
    selector = x.get_args(card)[0]
    targets = x.get_targets(card, selector)
    if isinstance(selector, fireplace.dsl.selector.FuncSelector) and len(targets) == 1 and targets[0] == card:
        currEffect["CanAffectSelf"] = 1
    times = x.times
    if isinstance(times, LazyValue):
        times = times.evaluate(card)
        currEffect["SetAmount"] = 0
    else:
        currEffect["SetAmount"] = 1
    if x._kwargs != {}:
        currEffect["SetAmount"] = 0
    buff = x.get_target_args(card, card)[0]
    if hasattr(buff.data.scripts, "apply"):
        currEffect["setsAttackToHealth"] = 1
    # hard coding- only inner fire has this
    if hasattr(buff.data.scripts, "max_health"):
        pass
    if currEffect.get("setsAttackToHealth") is None:
        currEffect["selfAttackValue"] = buff.atk * times
        currEffect["selfHealthValue"] = buff.max_health * times
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
                    currEffect["selfAttackValue"] = buff.data.scripts.atk(0, 1)
                if hasattr(buff.data.scripts, "max_health"):
                    currEffect["selfHealthValue"] = buff.data.scripts.max_health(0, 1)
                # hard coding divine spirit
                if "max_health" in x._kwargs:
                    currEffect["selfHealthValue"] = 2

        else:
            currEffect["AddValue"] = 1
            currEffect["SetValue"] = 0
            currEffect["MultiplyValue"] = 0
        currEffect["Permanent"] = 1 if int(buff.one_turn_effect) == 0 else 1
    else:
        currEffect["Permanent"] = 1
        currEffect["AddValue"] = 1


def decodeFuncSelector(func):
    if func == fireplace.dsl.selector.SELF:
        return " SELF "
    if func == fireplace.dsl.selector.TARGET:
        return " TARGET "
    if func == fireplace.dsl.selector.OTHER_CLASS_CHARACTER:
        return " OTHER_CLASS "
    if func == fireplace.dsl.selector.FRIENDLY_CLASS_CHARACTER:
        return " FRIENDLY_CLASS "
    if func == fireplace.dsl.selector.LEFTMOST_HAND:
        return " LEFTMOST_HAND "
    if func == fireplace.dsl.selector.RIGHTMOST_HAND:
        return " RIGHTMOST_HAND "
    if func == fireplace.dsl.selector.OWNER:
        return " OWNER "
    if func == fireplace.dsl.selector.ATTACK_TARGET:
        return " ATTACK TARGET "

def decodeOp(op):
    if op == operator.or_:
        return "|"
    if op == operator.add:
        return "?+?"
    if op == operator.and_:
        return "*"
    if op == operator.sub:
        return "-"
    if op == operator.eq:
        return "=="
    if op == operator.le:
        return "<="
    return ">O<"

def decodeEnum(enum):
    if isinstance(enum, str):
        return enum
    if enum == fireplace.dsl.selector.Zone.PLAY:
        return " : "
    if enum == fireplace.dsl.selector.CardType.MINION:
        return " M "
    if enum == fireplace.dsl.selector.CardType.HERO: #na hero sie gra np leczenie/buffa
        return " H "
    if enum == fireplace.dsl.selector.CardType.PLAYER: #na gracza sie gra np przyzwanie(przyzwij minionka)
        return " P "
    if enum == fireplace.dsl.selector.GameTag.CONTROLLER:
        return " C "
    if enum == fireplace.dsl.selector.GameTag.DORMANT:
        return " D "
    if enum == fireplace.dsl.selector.GameTag.DAMAGE:
        return " DMG "
    if enum == fireplace.dsl.selector.GameTag.SECRET:
        return " SEC "
    if enum == fireplace.dsl.selector.Zone.SECRET:
        return " ZSC "
    return ">E<"

def decodeController(controller):
    if isinstance(controller, fireplace.dsl.selector.Opponent):
        return " Opponent "
    else:
        return " Self "

def decodeBoardPosition(direction):
    if direction == fireplace.dsl.selector.BoardPositionSelector.Direction.LEFT:
        return " L"
    elif direction == fireplace.dsl.selector.BoardPositionSelector.Direction.RIGHT:
        return " R"
    else:
        return " >D<"

def decodeTarget(target):
    if target is None:
        return " NULL "
    if isinstance(target, fireplace.dsl.selector.RandomSelector):
        return "RANDOM "+"("+decodeTarget(target.child)+")" + "  T:"+str(target.times)

    if isinstance(target, fireplace.dsl.selector.SetOpSelector):
        return "("+decodeTarget(target.left)+")" + decodeOp(target.op) + "("+decodeTarget(target.right)+")"

    if isinstance(target, fireplace.dsl.selector.EnumSelector):
        return decodeEnum(target.tag_enum)

    if isinstance(target, fireplace.dsl.selector.ComparisonSelector):
        return "("+decodeTarget(target.left)+")" + decodeOp(target.op) + "("+decodeTarget(target.right)+")"

    if isinstance(target, fireplace.dsl.selector.AttrValue):
        return decodeEnum(target.tag)
    if isinstance(target, fireplace.dsl.selector.Controller):
        return decodeController(target)
    if isinstance(target, fireplace.dsl.selector.FuncSelector):
        return decodeFuncSelector(target)
    if isinstance(target, int):
        return str(target)
    if isinstance(target, fireplace.dsl.selector.BoardPositionSelector):
        return decodeBoardPosition(target.direction)+"("+decodeTarget(target.child)+")"
    return " Unknown "


def decodeFuncSelector2(func):
    if func == fireplace.dsl.selector.SELF:
        return 1 << 25
    if func == fireplace.dsl.selector.TARGET:
        return ~0
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

def decodeOp2(left, op, right):
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

def decodeEnum2(enum):
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

def decodeController2(controller):
    if isinstance(controller, fireplace.dsl.selector.Opponent):
        return ~(1 << 23) & ~(1 << 25)
    else:
        return ~(1 << 24)

def decodeBoardPosition2(direction):
    if direction == fireplace.dsl.selector.BoardPositionSelector.Direction.LEFT:
        return 1 << 28
    elif direction == fireplace.dsl.selector.BoardPositionSelector.Direction.RIGHT:
        return 1 << 27
    else:
        return " >D<"

# 1 << 31 oznacza random
# ostatnie 4 bity(czyli max. 16) oznaczają 'times' czyli ile celów losuje
# jeśli target.times będzie >=16 to mam nadzieję że tak nie będzie bo się spowrotem wyzeruje
def decodeTarget2(target):
    if target is None:
        return 0 #unknown value(co to znaczy w ogóle ze target is none)
    if isinstance(target, fireplace.dsl.selector.RandomSelector):
        return (1 << 31)+decodeTarget2(target.child)+(target.times%16)

    if isinstance(target, fireplace.dsl.selector.SetOpSelector):
        return decodeOp2(decodeTarget2(target.left), target.op, decodeTarget2(target.right))

    if isinstance(target, fireplace.dsl.selector.EnumSelector):
        return decodeEnum2(target.tag_enum)

    if isinstance(target, fireplace.dsl.selector.ComparisonSelector):
        return decodeOp2(decodeTarget2(target.left), target.op, decodeTarget2(target.right))

    if isinstance(target, fireplace.dsl.selector.AttrValue):
        return decodeEnum2(target.tag)
    if isinstance(target, fireplace.dsl.selector.Controller):
        return decodeController2(target)
    if isinstance(target, fireplace.dsl.selector.FuncSelector) | isinstance(target, fireplace.dsl.selector.FilterSelector):
        return decodeFuncSelector2(target)
    if isinstance(target, int):
        return 0
    if isinstance(target, fireplace.dsl.selector.BoardPositionSelector):
        return decodeBoardPosition2(target.direction)
    return " Unknown " #wyjatek i dobrze

def decodeResult(result):
    if result & 1 << 31:
        print("Random")
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
    print("Tyle razy: " + str(result & 0b1111))


def mapEndOfTurn(card):
    endOfTurnEffect = {}

    for x in card.data.scripts.events:
        if isinstance(x, fireplace.actions.EventListener) and isinstance(x.trigger, fireplace.actions.EndTurn):
            print("znalazlem end turn efekt u "+card.data.strings[GameTag.CARDNAME]['enUS'])
            for y in x.actions:
                result = 0
                if isinstance(y, fireplace.dsl.Find) | isinstance(y, fireplace.dsl.Dead):
                    print("TO JEST FIND")
                    result = decodeTarget2(y.selector)
                    print(decodeTarget(y.selector))
                else:
                    result = decodeTarget2(y._args[0])
                    print(decodeTarget(y._args[0]))

                print("0bR00LRCSEAMH00000000000000000TIME")
                print(bin(result).zfill(34))
                decodeResult(result)
                if isinstance(y, fireplace.actions.Hit):
                    print("Znalazlem damage "+str(y._args[1]))
                    endOfTurnEffect["Damage"] = y._args[1]
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
        getTargetedActionDetails(x,onAttackEffect,card)
    # loop for detecting what combo does
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
