class Hero:
    def __init__(self, character):
        self.player = character


    def mapToInput(self):
        hero = [0]*36
        weapon = [0]*3
        weapon[0] = self.player.weapon.atk
        weapon[1] = self.player.weapon.durability
        weapon[2] = self.player.weapon.cost
        hero[0] = 0
        hero[1] = self.player.characters[0].health
        hero[2] = self.player.characters[0].atk
        hero[3] = 30
        hero[4] = 0
        hero[5] = self.player.characters[0].exhausted
        hero[6] = 1 if self.player.characters[0].frozen else 0
        hero[7] = 0
        hero[8] = 0
        hero[9] = 1 if self.player.characters[0].taunt else 0
        hero[10] = 0
        hero[11:18] = 0
        hero[19] = len(self.player.characters[0].buffs)
        hero[20:22] = 0
        hero[23]
        hero[24]
        hero[25]
        hero[26]
        hero[27]
        hero[28] = 1 if self.player.characters[0].health < 30 else 0
        hero[29] = 1 if self.player.characters[0].windfury > 0 else 0
        hero[30] = 1 if self.player.characters[0].lifesteal else 0
        hero[31] = 1 if self.player.weapon is None else 0
        hero[32] = 1 if self.player.characters[0].immune else 0
        hero[33] = 1 if self.player.characters[0].cant_attack else 0
        hero[34] = self.player.characters[0].armor
        hero[35] = int(self.player.card_id[5:7])
        hero[36] = 1 if self.player.characters[0].poisonous else 0
        hero[37] = len(self.player.secrets)
