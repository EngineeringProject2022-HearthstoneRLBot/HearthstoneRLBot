class P:
    FIRST = 0
    SECOND = 1
    ANY = 2
    def __init__(self):
        self.p = P.ANY
        self.children = []
    def AND(self, f):
        return PAnd(self, f)
    def OR(self, f):
        return POr(self, f)
    def PLAYER(self, player):
        self.p = player
        if len(self.children) == 0:
            return
        for child in self.children:
            child.PLAYER(player)
    def WINS(self):
        tempFunc = self.func
        self.func = lambda winner, h, model, sim, deck: \
                        winner in (1,2) and (self.p == 2 or (winner-1 == self.p) and (tempFunc(winner, h, model, sim, deck) if tempFunc else True))
        return self
    def LOSES(self):
        tempFunc = self.func
        self.func = lambda winner, h, model, sim, deck: \
                        winner in (1,2) and (self.p == 2 or (winner-1 == (not self.p)) and (tempFunc(winner, h, model, sim, deck) if tempFunc else True))
        return self
    def __call__(self, *args):
        return self.func(*args)

class PAnd(P):
    def __init__(self, f1, f2):
        super().__init__()
        self.children.extend([f1,f2])
        self.func = lambda *args: f1(*args) and f2(*args)

class POr(P):
    def __init__(self, f1, f2):
        super().__init__()
        self.children.extend([f1,f2])
        self.func = lambda *args: f1(*args) or f2(*args)

class PNot(P):
    def __init__(self, f):
        super().__init__()
        self.children.extend([f])
        self.func = lambda *args: not f(*args)

class PHero(P):
    def __init__(self, hero):
        super().__init__()
        self.hero = hero
    def func(self, winner, h, model, sim, deck):
        if self.p==P.ANY:
            return self.hero in h
        return h[self.p] == self.hero

class PModel(P):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def func(self, winner, h, model, sim, deck):
        if self.p == P.ANY:
            return self.model in model
        return model[self.p] == self.model

class PDeck(P):
    def __init__(self, deck):
        super().__init__()
        self.deck = deck
    def func(self, winner, h, model, sim, deck):
        if self.p == P.ANY:
            return self.deck in deck
        return deck[self.p] == self.deck

class PMirrorDeck(P):
    def func(self, winner, h, model, sim, deck):
        return deck[0] == deck[1]

class PMirrorHero(P):
    def func(self, winner, h, model, sim, deck):
        return h[0] == h[1]

class PSimulations(P):
    def __init__(self, value = None):
        self.gt = float('-inf')
        self.lt = float('inf')
        self.eq = value

    def func(self, winner, h, model, sim, deck):
        if self.p == P.ANY:
            return  self.lt < sim[0] < self.gt and (self.eq is None or sim[0] == self.eq) \
                    or \
                    self.lt < sim[1] < self.gt and (self.eq is None or sim[1] == self.eq)
        return self.lt < sim[self.p] < self.gt and (self.eq is None or sim[self.p] == self.eq)

    def GREATERTHAN(self, value):
        self.gt = value
        return self
    def LOWERTHAN(self, value):
        self.lt = value
        return self
    def EQUALS(self, value):
        self.eq = value


class PValid(P):
    def func(self, winner, h, model, sim, deck):
        return winner == 1 or winner == 2 or winner == 3


class PDraws(P):
    def func(self, winner, h, model, sim, deck):
        return winner == 3


class PPlayer(P):
    def __init__(self, num):
        super().__init__()
        self.p = num
        self.func = None
    def HAS(self, func):
        func.PLAYER(self.p)
        self.func = func
        return self