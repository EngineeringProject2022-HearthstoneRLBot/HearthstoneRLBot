import fireplace
from fireplace.dsl import LazyValue


class HandCard:

    def __init__(self, card):
        self.card = card
        self.cost = 0
        self.currentHealth = 0
        self.currentAttack = 0
        self.baseHealth = 0
        self.baseAtt = 0
        self.sleeping = 0
        self.frozen = 0
        self.charge = 0
        self.rush = 0
        self.taunt = 0
        self.divineShield = 0
        self.isNoneType = 0
        self.isMurloc = 0
        self.isPirate = 0
        self.isTotem = 0
        self.isBeast = 0
        self.isDemon = 0
        self.isDragon = 0
        self.isMech = 0
        self.isElemental = 0
        self.isBuffed = 0
        self.hasDeathrattle = 0
        self.hasBattlecry = 0
        self.hasAura = 0
        self.hasCondEff = 0
        self.hasEoTEff = 0
        self.hasSoTEff = 0
        self.spellDamage = 0
        self.stealth = 0
        self.isDamaged = 0
        self.windfury = 0
        self.position = 0
        self.isWeapon = 0
        self.isImmune = 0
        self.cantAttack = 0
        self.cantAttackHeroes = 0
        self.armor = 0
        self.cantBeAttacked = 0
        self.isSecret = 0

        #ciekawsze kombinacje:
        self.deathrattle = []
        self.activate = []
        self.awaken = []
        self.combo = []
        self.costMod = []
        self.draw = []
        self.enrage = []
        self.events = []
        self.inspire = []
        self.outcast = []
        self.play = []
        self.poweredUp = []
        self.secret = []
        self.update = []

        self.buffs = []
        self.requirements = {}

        #### Fetching actual data ####
        #self.currentAttack = card.atk


    def mapToInput(self):
        for x in self.play:
            if isinstance(x, fireplace.actions.Buff):
                selector = x.get_args(self.card)[0]
                times = x.times
                if isinstance(times, LazyValue):
                    times = times.evaluate(self.card)
                if self.card in x.get_targets(self.card,selector):
                    buff = x.get_target_args(self.card,self.card)[0]
                    value = buff.max_health * times


