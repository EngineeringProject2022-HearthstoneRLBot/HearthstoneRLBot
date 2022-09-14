import types

import fireplace
import numpy as np
from fireplace.actions import SetTag, Silence, Heal, Hit, Destroy, GainArmor, Draw, Discard, Summon, Bounce, \
    ManaThisTurn, GainMana, SpendMana
from fireplace.card import Card
from fireplace.dsl import RandomEntourage, LazyValue
from hearthstone.enums import GameTag

from GameState.TargetDecoder import decodeWithRequirements, decodeTarget


def encode_complex_plane(dictionary):
    arr = np.zeros(169)
    arr[0] = dictionary.get("HealthValue", 0)
    arr[1] = dictionary.get("AttackValue", 0)
    arr[2] = dictionary.get("setsHealthToAttack", 0)
    arr[3] = dictionary.get("setsAttackToHealth", 0)
    arr[4] = dictionary.get("SetValue", 0)
    arr[5] = dictionary.get("MultiplyValue", 0)
    arr[6] = dictionary.get("AddValue", 0)
    arr[7] = dictionary.get("GiveTaunt", 0)
    arr[8] = dictionary.get("GiveDivShield", 0)
    arr[9] = dictionary.get("GivePoison", 0)
    arr[10] = dictionary.get("GiveStealth", 0)
    arr[11] = dictionary.get("GiveSilence", 0)
    arr[12] = dictionary.get("Freeze", 0)
    # I miscounted and cannot be bothered right now to correct. So i have added a
    # perimeter to determine the length of
    # target padding which here is changed to 17 from the default 16
    arr[13:30] = encode_targets(dictionary.get("BuffTargets"), 17)
    arr[30] = dictionary.get("UnknownAmount", 0)
    always = dictionary.get("AlwaysGetBuff")
    if always is not None:
        if always == 0:
            arr[31] = 1
        else:
            arr[32] = 1
    set = dictionary.get("SetAmount")
    if set is not None:
        if set == 0:
            arr[34] = 1
        else:
            arr[33] = 1
    permanent = dictionary.get("Permanent")
    if permanent is not None:
        if permanent == 0:
            arr[36] = 1
        else:
            arr[36] = 1
    arr[37] = dictionary.get("DiscardCards", 0)
    if arr[37] == 1:
        arr[38] = dictionary.get("DiscardCardsTimes")
        # TODO only return the 2 relevant fields
        arr[40:42] = encode_targets(dictionary.get("DiscardTargets"))[3:5]
        arr[39] = dictionary.get("UnknownAmountDiscard", 0)
        set = dictionary.get("SetAmountDiscard")
        if set is not None:
            if set == 0:
                arr[43] = 1
            else:
                arr[42] = 1
        always = dictionary.get("AlwaysGetDiscard")
        if always is not None:
            if always == 0:
                arr[45] = 1
            else:
                arr[44] = 1
    arr[46] = dictionary.get("HitAmount", 0)
    arr[47:63] = encode_targets(dictionary.get("HitTargets"))
    arr[63] = dictionary.get("UnknownAmountHit", 0)
    always = dictionary.get("AlwaysGetHit")
    if always is not None:
        if always == 0:
            arr[65] = 1
        else:
            arr[64] = 1
    set = dictionary.get("SetAmountHit")
    if set is not None:
        if set == 0:
            arr[67] = 1
        else:
            arr[66] = 1
    arr[68] = dictionary.get("HealAmount", 0)
    arr[69:85] = encode_targets(dictionary.get("HealTargets"))
    arr[85] = dictionary.get("UnknownAmountHeal", 0)
    always = dictionary.get("AlwaysGetHeal")
    if always is not None:
        if always == 0:
            arr[87] = 1
        else:
            arr[86] = 1
    set = dictionary.get("SetAmountHeal")
    if set is not None:
        if set == 0:
            arr[89] = 1
        else:
            arr[88] = 1
    if dictionary.get("Destroy", 0) == 1:
        arr[90] = 1
        arr[91:107] = encode_targets(dictionary.get("DestroyTargets"))
        arr[107] = dictionary.get("UnknownAmountDestroy", 0)
        always = dictionary.get("AlwaysGetDestroy")
        if always is not None:
            if always == 0:
                arr[109] = 1
            else:
                arr[108] = 1
        set = dictionary.get("SetAmountDestroy")
        if set is not None:
            if set == 0:
                arr[111] = 1
            else:
                arr[110] = 1
    if dictionary.get("Summon", 0) == 1:
        arr[112] = 1
        arr[113] = dictionary.get("SummonTimes", 0)
        arr[114] = dictionary.get("UnknownAmountSummon", 0)
        arr[115:117] = encode_targets(dictionary.get("SummonTargets"))[3:5]
        arr[117] = dictionary.get("SummonedAvgAttack", 0)
        arr[118] = dictionary.get("SummonedAvgHealth", 0)
        arr[119] = dictionary.get("SummonedAvgCost", 0)
        always = dictionary.get("AlwaysGetSummon")
        if always is not None:
            if always == 0:
                arr[121] = 1
            else:
                arr[120] = 1
        set = dictionary.get("SetAmountSummon")
        if set is not None:
            if set == 0:
                arr[123] = 1
            else:
                arr[122] = 1
        arr[124] = dictionary.get("UnknownSummon", 0)
        arr[125] = dictionary.get("WeaponSummon", 0)
        arr[126] = dictionary.get("SummonFromEntourage", 0)
    arr[127] = dictionary.get("GainArmorAmount", 0)
    arr[128] = dictionary.get("UnknownAmountArmor", 0)
    arr[129:131] = encode_targets(dictionary.get("GainArmorTargets"))[3:5]
    always = dictionary.get("AlwaysGetSummon")
    if always is not None:
        if always == 0:
            arr[132] = 1
        else:
            arr[131] = 1
    set = dictionary.get("SetAmountSummon")
    if set is not None:
        if set == 0:
            arr[134] = 1
        else:
            arr[133] = 1
    if dictionary.get("BounceCards", 0):
        arr[135] = 1
        arr[136:152] = encode_targets(dictionary.get("BounceTargets"))
        arr[152] = dictionary.get("UnknownAmountBounce", 0)
        arr[153] = dictionary.get("GainManaCrystal", 0)
        arr[154:156] = encode_targets(dictionary.get("GainManaCrystalTargets"))[3:5]
        arr[156] = dictionary.get("ManaCrystalEmpty", 0)
        arr[157] = dictionary.get("ManaCrystalFull", 0)
        arr[158] = dictionary.get("ManaThisTurnOnly", 0)
        always = dictionary.get("AlwaysGetMana")
        if always is not None:
            if always == 0:
                arr[160] = 1
            else:
                arr[159] = 1
        set = dictionary.get("SetAmountMana")
        if set is not None:
            if set == 0:
                arr[162] = 1
            else:
                arr[161] = 1
        arr[163] = dictionary.get("UnknownAmountMana")

    return arr


def encode_targets(target, length=16):
    arr = np.zeros(length)
    if target is None:
        return arr
    else:
        arr[0] = (target & 1 << 25) > 0  # self
        arr[1] = (target & 1 << 21) > 0  # herosy
        arr[2] = (target & 1 << 22) > 0  # miniony
        arr[3] = (target & 1 << 23) > 0  # our
        arr[4] = (target & 1 << 24) > 0  # enemy
        arr[5] = ((target & (1 << 27)) > 0) and ((target & (1 << 28)) > 0)  # adjacenty
        arr[6] = not ((target & 1 << 31) > 0) and ((target & 1 << 26) > 0)  # nie jest randomem i nie jest conditionalem
        arr[7] = not ((target & 1 << 31) > 0) and not ((target & 1 << 26) > 0)  # nie jest randomem i jest conditionalem
        arr[9] = target & 0b1111  # ile razy
        arr[8] = (target & 1 << 31) > 0 and arr[
            9] > 1  # jesli jest randomem i ileś razy z subsetu to bedzie differnt each time
        arr[10] = not ((target & 1 << 31) > 0) and not arr[6] and not arr[7] and not arr[
            0]  # jesli nie jest randomem i nie efektuje wszystkich z subsetu
        # print(arr)
        # decodeResultStr(target)
        return arr


def mapBattlecrySpells(card):
    currentBattlecryEffect = {}
    # if len(card.requirements) != 0:
    #     for x in card.data.scripts.requirements:
    #         if type(x) is PlayReq and x is not PlayReq.REQ_TARGET_TO_PLAY:
    #             currentBattlecryEffect["AlwaysGet"] = 0
    #             break
    try:
        if not isinstance(card.data.scripts.play, types.FunctionType):
            for x in card.data.scripts.play:
                getTargetedActionDetails(x, currentBattlecryEffect, card)
        else:
            for x in card.data.scripts.play(card):
                getTargetedActionDetails(x, currentBattlecryEffect, card)
    except TypeError:
        None
    return currentBattlecryEffect

    # TODO


def getTargetedActionDetails(x, currentBattlecryEffect, card):
    while hasattr(x, "_if"):
        # isinstance(x, fireplace.dsl.evaluator.Find):
        currentBattlecryEffect["AlwaysGet"] = 0
        if x._if is None:
            x = x._else
        elif x._else is None:
            x = x._if
        else:
            getTargetedActionDetails(x._else, currentBattlecryEffect, card)
            x = x._if
    else:
        if "AlwaysGet" not in currentBattlecryEffect:
            currentBattlecryEffect["AlwaysGet"] = 1

    # if isinstance(x, fireplace.dsl.evaluator.Dead):
    #     selector = x.selector
    # elif isinstance(x, fireplace.dsl.LazyNumEvaluator):
    #     selector = x.num.selector
    # else:
    if type(x) is tuple:
        for element in x[1:]:
            getTargetedActionDetails(element, currentBattlecryEffect, card)
        x = x[0]
    if hasattr(x, "actions"):
        x = x.actions[-1]

    if hasattr(x, 'get_args') and len(x.get_args(card)) != 0:
        selector = x.get_args(card)[0]
    else:
        selector = None

    # targets = x.get_targets(card, selector)
    # if isinstance(selector, fireplace.dsl.selector.FuncSelector) and len(targets) == 1 and targets[0] == card:
    #    currentBattlecryEffect["CanAffectSelf"] = 1
    # elif isinstance(selector, fireplace.dsl.selector.FuncSelector) and targets[0] is None:
    #    currentBattlecryEffect["IChooseCard"] = 1
    # else:

    if isinstance(x, fireplace.actions.Buff):
        currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        getBuffDetails(x, currentBattlecryEffect, card)
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysBuff"] = 0
        else:
            currentBattlecryEffect["AlwaysGetBuff"] = 1
    elif isinstance(x, SetTag):
        if GameTag.DIVINE_SHIELD in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector),
                                                                           card.data.requirements)
            currentBattlecryEffect["GiveDivShield"] = 1
            if currentBattlecryEffect["AlwaysGet"] == 0:
                currentBattlecryEffect["AlwaysBuff"] = 0
            else:
                currentBattlecryEffect["AlwaysGetBuff"] = 1
        if GameTag.TAUNT in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector),
                                                                           card.data.requirements)
            currentBattlecryEffect["GiveTaunt"] = 1
            if currentBattlecryEffect["AlwaysGet"] == 0:
                currentBattlecryEffect["AlwaysBuff"] = 0
            else:
                currentBattlecryEffect["AlwaysGetBuff"] = 1
        if GameTag.STEALTH in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector),
                                                                           card.data.requirements)
            currentBattlecryEffect["GiveStealth"] = 1
            if currentBattlecryEffect["AlwaysGet"] == 0:
                currentBattlecryEffect["AlwaysBuff"] = 0
            else:
                currentBattlecryEffect["AlwaysGetBuff"] = 1
        if GameTag.POISONOUS in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector),
                                                                           card.data.requirements)
            currentBattlecryEffect["GivePoison"] = 1
            if currentBattlecryEffect["AlwaysGet"] == 0:
                currentBattlecryEffect["AlwaysBuff"] = 0
            else:
                currentBattlecryEffect["AlwaysGetBuff"] = 1
        if GameTag.FROZEN in x._args[1]:
            currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector),
                                                                           card.data.requirements)
            currentBattlecryEffect["Freeze"] = 1
            if currentBattlecryEffect["AlwaysGet"] == 0:
                currentBattlecryEffect["AlwaysBuff"] = 0
            else:
                currentBattlecryEffect["AlwaysGetBuff"] = 1
    elif isinstance(x, Silence):
        currentBattlecryEffect["BuffTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["GiveSilence"] = 1
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysBuff"] = 0
        else:
            currentBattlecryEffect["AlwaysGetBuff"] = 1
    elif isinstance(x, Heal):
        currentBattlecryEffect["HealTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["HealAmount"] = getAmount(x, card, currentBattlecryEffect, "Heal")
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetHeal"] = 0
        else:
            currentBattlecryEffect["AlwaysGetHeal"] = 1
    elif isinstance(x, Hit):
        currentBattlecryEffect["HitTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)
        currentBattlecryEffect["HitAmount"] = getAmount(x, card, currentBattlecryEffect, "Hit")
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetHit"] = 0
        else:
            currentBattlecryEffect["AlwaysGetHit"] = 1
    elif isinstance(x, Destroy):
        currentBattlecryEffect["DestroyTargets"] = decodeWithRequirements(decodeTarget(selector),
                                                                          card.data.requirements)
        currentBattlecryEffect["Destroy"] = 1
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetDestroy"] = 0
        else:
            currentBattlecryEffect["AlwaysGetDestroy"] = 1
    elif isinstance(x, GainArmor):
        currentBattlecryEffect["GainArmorTargets"] = decodeWithRequirements(decodeTarget(selector),
                                                                            card.data.requirements)
        currentBattlecryEffect["GainArmorAmount"] = getAmount(x, card, currentBattlecryEffect, "Armor")
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetArmor"] = 0
        else:
            currentBattlecryEffect["AlwaysGetArmor"] = 1
    elif isinstance(x, Draw):
        currentBattlecryEffect["DrawCardsTargets"] = decodeWithRequirements(decodeTarget(selector),
                                                                            card.data.requirements)
        currentBattlecryEffect["DrawCards"] = 1
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetDraw"] = 0
        else:
            currentBattlecryEffect["AlwaysGetDraw"] = 1
    elif isinstance(x, Discard):
        currentBattlecryEffect["DiscardTargets"] = decodeWithRequirements(decodeTarget(selector),
                                                                          card.data.requirements)
        currentBattlecryEffect["DiscardCards"] = 1
        currentBattlecryEffect["DiscardCardsTimes"] = getTimes(x, card, currentBattlecryEffect, "Discard")
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetDiscard"] = 0
        else:
            currentBattlecryEffect["AlwaysGetDiscard"] = 1
    elif isinstance(x, Summon):
        getSummonDetails(x, card, currentBattlecryEffect)
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetSummon"] = 0
        else:
            currentBattlecryEffect["AlwaysGetSummon"] = 1
    elif isinstance(x, Bounce):
        currentBattlecryEffect["BounceTargets"] = decodeTarget(selector)
        currentBattlecryEffect["BounceCards"] = 1
    elif isinstance(x, ManaThisTurn):
        currentBattlecryEffect["GainManaCrystalTargets"] = decodeTarget(selector)
        currentBattlecryEffect["GainManaCrystal"] = getAmount(x, card, currentBattlecryEffect, "Mana")
        currentBattlecryEffect["ManaCrystalFull"] = 1
        currentBattlecryEffect["ManaThisTurnOnly"] = 1
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetMana"] = 0
        else:
            currentBattlecryEffect["AlwaysGetMana"] = 1

    elif isinstance(x, GainMana):
        currentBattlecryEffect["GainManaCrystalTargets"] = decodeTarget(selector)
        currentBattlecryEffect["GainManaCrystal"] = getAmount(x, card, currentBattlecryEffect, "Mana")
        if currentBattlecryEffect.get("ManaCrystalEmpty") is None:
            currentBattlecryEffect["ManaCrystalFull"] = 1
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetMana"] = 0
        else:
            currentBattlecryEffect["AlwaysGetMana"] = 1

    elif isinstance(x, SpendMana):
        currentBattlecryEffect["GainManaCrystalTargets"] = decodeTarget(selector)
        currentBattlecryEffect["GainManaCrystal"] = getAmount(x, card, currentBattlecryEffect, "Mana")
        currentBattlecryEffect["ManaCrystalEmpty"] = 1
        if currentBattlecryEffect["AlwaysGet"] == 0:
            currentBattlecryEffect["AlwaysGetMana"] = 0
        else:
            currentBattlecryEffect["AlwaysGetMana"] = 1

    # if selector is not None:
    # decodeResultStr(decodeWithRequirements(decodeTarget(selector), card.data.requirements))


def getSummonDetails(x, card, currentEffect):
    selector = x.get_args(card)[0]
    currentEffect["Summon"] = 1
    currentEffect["SummonTimes"] = getTimes(x, card, currentEffect, "Summon")
    currentEffect["SummonTargets"] = decodeWithRequirements(decodeTarget(selector), card.data.requirements)

    try:
        toSummonID = x.get_args(card)[1]
        if type(toSummonID) is RandomEntourage:
            # TODO hmmm
            currentEffect["SummonFromEntourage"] = 1
            sum_health = 0
            sum_atk = 0
            sum_cost = 0
            for y in card.entourage:
                entourageMember = Card(y)
                sum_atk += entourageMember.atk
                sum_health += entourageMember.health
                sum_cost += entourageMember.cost
            currentEffect["SummonedAvgHealth"] = sum_health / len(card.entourage)
            currentEffect["SummonedAvgAttack"] = sum_atk / len(card.entourage)
            currentEffect["SummonedAvgCost"] = sum_cost / len(card.entourage)
            currentEffect["SummonedCalculatedValue"] = 1
        else:
            toSummon = Card(toSummonID)
            currentEffect["SummonedAvgAttack"] = toSummon.atk
            currentEffect["SummonedAvgCost"] = toSummon.cost
            if (type(toSummon) == fireplace.card.Weapon):
                currentEffect["WeaponSummon"] = 1
                currentEffect["SummonedAvgHealth"] = toSummon.durability
            else:
                currentEffect["SummonedAvgHealth"] = toSummon.health
    except:
        currentEffect["UnknownSummon"] = 1
    currentEffect["SummonTargets"] = decodeTarget(selector)


def getAmount(x, card, currEffect, key):
    if type(x.get_args(card)[-1]) is not int:
        # print("DEPENDANT SOMETHING FOUND!!!")
        currEffect["SetAmount" + key] = 0
        try:
            return x.get_args(card)[-1].evaluate(card)
        except:
            currEffect["UnknownAmount" + key] = 1
            return 0
    else:
        currEffect["SetAmount" + key] = 1
        return x.get_args(card)[-1]


def getTimes(x, card, currEffect, key):
    times = x.times
    if isinstance(times, LazyValue) or type(times) is not int:
        try:
            times = times.evaluate(card)
        except:
            currEffect["UnknownAmount" + key] = 1
            times = 0
        currEffect["SetAmount" + key] = 0
    else:
        currEffect["SetAmount" + key] = 1
    return times


def getBuffDetails(x, currEffect, card):
    times = 0
    if hasattr(x, "times"):
        times = getTimes(x, card, currEffect, "")
    if x._kwargs != {}:
        currEffect["SetAmount"] = 0
    buff = x.get_target_args(card, card)[0]
    # hard coding- only inner fire has this
    if hasattr(buff.data.scripts, "apply"):
        currEffect["setsAttackToHealth"] = 1
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
        if hasattr(buff, "one_turn_effect"):
            currEffect["Permanent"] = 1 if int(buff.one_turn_effect) == 0 else 0
        else:
            currEffect["Permanent"] = 1
    else:
        currEffect["Permanent"] = 1
        currEffect["AddValue"] = 1


def mapEndOfTurn(card):
    endOfTurnEffect = {}

    for x in card.data.scripts.events:
        if isinstance(x.trigger, fireplace.actions.EndTurn):
            for y in x.actions:
                getTargetedActionDetails(y, endOfTurnEffect, card)

    return endOfTurnEffect


def mapConditional(card):
    conditionalEffect = {}

    # loop for detecting what combo does
    for x in card.data.scripts.combo:
        # effect = card.get_actions("combo")[0].get_target_args(card, card)[0]
        conditionalEffect["AlwaysGet"] = 0
        getTargetedActionDetails(x, conditionalEffect, card)

    for x in card.data.scripts.events:
        if isinstance(x.trigger, fireplace.actions.Death):
            getTargetedActionDetails(x.actions[0], conditionalEffect, card)
        if isinstance(x.trigger, fireplace.actions.Hit):
            getTargetedActionDetails(x.actions[0], conditionalEffect, card)
        if isinstance(x.trigger, fireplace.actions.Draw):
            getTargetedActionDetails(x.actions[0], conditionalEffect, card)
        if isinstance(x.trigger, fireplace.actions.Heal):
            getTargetedActionDetails(x.actions[0], conditionalEffect, card)
        if isinstance(x.trigger, fireplace.actions.Play):
            getTargetedActionDetails(x.actions[0], conditionalEffect, card)
        if isinstance(x.trigger, fireplace.actions.Summon):
            getTargetedActionDetails(x.actions[0], conditionalEffect, card)

    return conditionalEffect
    # TODO


def mapStartOfTurn(card):
    startOfTurnEffect = {}
    for x in card.data.scripts.events:
        if isinstance(x.trigger, fireplace.actions.BeginTurn):
            for y in x.actions:
                getTargetedActionDetails(y, startOfTurnEffect, card)
    return startOfTurnEffect


def mapOnAttack(card):
    onAttackEffect = {}
    if card.type == 5:
        return onAttackEffect
    # snowchugger
    # cutpurse ale nie ma go chyba w kartach
    # alley armorsmith
    for x in card.data.scripts.enrage:
        getTargetedActionDetails(x, onAttackEffect, card)

    for x in card.data.scripts.events:
        if isinstance(x, fireplace.actions.EventListener):
            if isinstance(x.trigger, fireplace.actions.Damage):
                getTargetedActionDetails(x, onAttackEffect, card)
                # print("On attack effect (event Damage)")
    return onAttackEffect


def mapDeathrattle(card):
    deathrattleEffect = {}
    if card.type == 5:
        return deathrattleEffect
    found = False
    for x in card.data.scripts.deathrattle:
        found = True
        deathrattleEffect["AlwaysGet"] = 1
        getTargetedActionDetails(x, deathrattleEffect, card)

    if not found and hasattr(card, "deathrattles"):

        for x in card.deathrattles:
            deathrattleEffect["AlwaysGet"] = 1
            getTargetedActionDetails(x, deathrattleEffect, card)

    return deathrattleEffect