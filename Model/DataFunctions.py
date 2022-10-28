from math import exp

from GameFiles.DataProvider import STurn

def diminishingValue(turn : STurn, min_v=0.3, steep=8):
    w = turn.pRef.winner-turn.pRef.loser
    l = len(turn.pRef.game.turns)
    x = l-turn.id
    y = min_v + (1-min_v)/(1+exp(steep*x/l - steep/2))
    return w*y
