import operator

import fireplace
from hearthstone.enums import PlayReq

# 1 << 31 oznacza random
# ostatnie 4 bity(czyli max. 16) oznaczają 'times' czyli ile celów losuje
# jeśli target.times będzie >=16 to mam nadzieję że tak nie będzie bo się spowrotem wyzeruje



def decodeWithRequirements(result, requirements):
    if PlayReq.REQ_MINION_TARGET in requirements:
        result = result & (~(1 << 21))
    if PlayReq.REQ_HERO_TARGET in requirements:
        result = result & (~(1 << 22))
    if PlayReq.REQ_FRIENDLY_TARGET in requirements:
        result = result & (~(1 << 24))
    if PlayReq.REQ_ENEMY_TARGET in requirements:
        result = result & (~(1 << 23)) & (~(1 << 25))
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
        return "?+?"  # tu chce wyjatek bo tego chyba nie bedzie
    if op == operator.and_:
        return left & right
    if op == operator.sub:
        return left & (~right)
    if op == operator.eq:
        return left | right  # nie wiem w sumie
    if op == operator.le:
        return left | right  # nie wiem w sumie
    return ">O<"


def decodeEnum(enum):
    if isinstance(enum, str):
        return 0
    if enum == fireplace.dsl.selector.Zone.PLAY:
        return ~0
    if enum == fireplace.dsl.selector.CardType.MINION:
        return 1 << 22 | 1 << 23 | 1 << 24 | 1 << 25 | 1 << 26  # czy na self mogę zagra
    if enum == fireplace.dsl.selector.CardType.HERO:  # na hero sie gra np leczenie/buffa
        return 1 << 21 | 1 << 23 | 1 << 24 | 1 << 26
    if enum == fireplace.dsl.selector.CardType.PLAYER:  # na gracza sie gra np przyzwanie(przyzwij minionka)
        return (1 << 23) | (1 << 24) | 1 << 26  # aktywuję self i enemy aby pozniej kontroler mogl cos wylaczyc
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


def decodeTarget(target):
    if target is None:
        return 0  # unknown value(co to znaczy w ogóle ze target is none)
    if isinstance(target, fireplace.dsl.selector.RandomSelector):
        return (1 << 31) + decodeTarget(target.child) + (target.times % 16)

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
    if isinstance(target, fireplace.dsl.selector.FuncSelector) | isinstance(target,
                                                                            fireplace.dsl.selector.FilterSelector):
        return decodeFuncSelector(target)
    if isinstance(target, int):
        return 0
    if isinstance(target, fireplace.dsl.selector.BoardPositionSelector):
        return decodeBoardPosition(target.direction)
    return 1 << 20  # 20 pozycja to unknown target


def decodeResultStr(result):
    if type(result) is str:
        print(result)
        return
    if result & 1 << 31:
        print("Random tyle razy: " + str(result & 0b1111))
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