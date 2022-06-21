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
        #Hero power needs to be implemented!

        print("")