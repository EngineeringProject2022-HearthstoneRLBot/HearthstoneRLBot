import glob
import pickle
import random

from GameInterface import GameData
from GameInterface.GameData import HeroDecks


class STurn:
    def __init__(self, id, sparseData, probs, action, pRef):
        self.id = id
        self.sparseData = sparseData
        self.probs = probs
        self.action = action
        self.pRef = pRef

class SPlayer:
    def __init__(self, name, winner, loser, game):
        self.deckname, self.hero, self.modelname, self.simulations = self.parseName(name)
        self.winner = winner
        self.loser = loser
        self.game = game

    def parseName(self, name):
        splitted = name[1:].split('_')
        deckname = splitted[0]
        modelname = splitted[1]
        simulations = int(splitted[2][11:]) if len(splitted) > 2 else -1
        return deckname, HeroDecks.HeroFromDeckName(deckname), modelname, simulations

class SGame:
    def __init__(self, id, gameElement):
        self.id = id
        self.p1, self.p2, self.winner, self.turns, self.exception = self.analyzeGameElement(gameElement)

    def analyzeGameElement(self, gameElement):
        turnElements = gameElement[0]
        winner = gameElement[1]
        player_data = gameElement[3]
        traceback = gameElement[4]
        p1 = SPlayer(player_data[6], winner == 1, winner == 2, self)
        p2 = SPlayer(player_data[7], winner == 2, winner == 1, self)
        turns = []
        for turnElement in turnElements:
            turns.append(self.analyzeTurnElement(len(turns), turnElement, p1, p2))
        return p1, p2, winner, turns, traceback

    def analyzeTurnElement(self, id, turnElement, p1, p2):
        input = turnElement[0]
        policy = turnElement[1]
        player = turnElement[2]
        action = turnElement[3]
        return STurn(id, input, policy, action, p1 if player == 1 else p2)

class TODO(Exception):
    pass
class DataProvider:
    def __init__(self, files, csv = False):
        if csv:
            raise TODO()
        self.games = []
        self.turns = []
        for filepath in files:
            with open(filepath, "rb") as rb:
                try:
                    # SKIP METADATA
                    pickle.load(rb)
                    while True:
                        game = pickle.load(rb)
                        sGame = SGame(len(self.games), game)
                        self.turns.extend(sGame.turns)
                        self.games.append(sGame)
                except EOFError:
                    print(f"EOF {filepath}")

    def getGamesWithPredicate(self, predicate):
        output = []
        for game in self.games:
            hp1 = game.p1.hero
            hp2 = game.p2.hero
            winner = game.winner
            mp1 = game.p1.modelname
            mp2 = game.p2.modelname
            simp1 = game.p1.simulations
            simp2 = game.p2.simulations
            deckp1 = game.p1.deckname
            deckp2 = game.p2.deckname
            if predicate(winner, [hp1, hp2], [mp1, mp2], [simp1, simp2], [deckp1, deckp2]):
                output.append(game)
        return output


    def getFirstGamesForEachClass(self, game_count):
        gamesForClass = []
        for hero in GameData.AllHeros:
            gamesForClass.extend(self.getFirstXGamesForClass(hero, game_count))
        return gamesForClass

    def getFirstXGamesForClass(self,hero,game_count):
        first_x_games = []
        counter = 0
        for game in self.games:
            if game_count == counter:
                return first_x_games
            if game.p1.hero == hero or game.p2.hero == hero:
                first_x_games.append(game)
                counter += 1
        return first_x_games

    def turn(self, tId):
        return self.turns[tId]

    def validIds(self):
        list = []
        for id, turn in enumerate(self.turns):
            if turn.pRef.winner or turn.pRef.loser:
                list.append(id)
        return list


    def balancedIds(self):
        counter = {}
        for id, turn in enumerate(self.turns):
            player = turn.pRef
            if (player.winner or player.loser) \
                    and not player.deckname in counter:
                counter[player.deckname] = [0, 0, [],[]]
            if player.winner:
                counter[player.deckname][0] += 1
                counter[player.deckname][2].append(id)
            if player.loser:
                counter[player.deckname][1] += 1
                counter[player.deckname][3].append(id)

        globalMin = float('inf')
        for value in counter.values():
            globalMin = min(globalMin, value[0], value[1])

        balancedListIds = []
        for value in counter.values():
            balancedListIds.extend(random.sample(value[2], globalMin))
            balancedListIds.extend(random.sample(value[3], globalMin))

        return balancedListIds

    def getAllModels(self):
        list = []
        for game in self.games:
            if game.p1.modelname not in list:
                list.append(game.p1.modelname)
            if game.p2.modelname not in list:
                list.append(game.p2.modelname)

    # def getSummaryByHero(self):
    #     models = self.getAllModels()
    #     for hero in Hero.AllHeros:
    #         for model in models:
    #             gamesByModel = self.getGamesWithPredicate(PHero(hero).AND(PModel(model)))


    @staticmethod
    def DataFromFolder(folder):
        return DataProvider([filepath for filepath in glob.iglob(f'data/{folder}/*')])

    @staticmethod
    def CSVFromFolder(folder):
        return DataProvider([filepath for filepath in glob.iglob(f'data/{folder}/*')], True)

    @staticmethod
    def DataFromFile(file):
        return DataProvider([f'data/{file}'])

    @staticmethod
    def CSVFromFile(file):
        return DataProvider([f'data/{file}'])


#
# dp = DataProvider.DataFromFolder('DEFAULT_OUTPUT')
#
# print(len(dp.games))
# sum0 = 0
# sum1 = 0
# for deck in GameData.HeroDecks.AllDecks:
#     g = dp.getGamesWithPredicate(PPlayer(P.FIRST).HAS(PDeck(deck[0])).WINS()
#                                  .OR(
#                                  PPlayer(P.SECOND).HAS(PDeck(deck[0])).WINS()
#     ))
#     g2 = dp.getGamesWithPredicate(PPlayer(P.FIRST).HAS(PDeck(deck[0]).LOSES())
#                                   .OR(
#                                   PPlayer(P.SECOND).HAS(PDeck(deck[0]).LOSES())
#     ))
#     print(deck[0], len(g), len(g2))
#     sum0 += len(g)
#     sum1 += len(g2)
# print(sum0, sum1)
# dp.getGamesWithPredicate(PPlayer(P.FIRST).WINS())
# x = dp.balancedIds()
#
# g0 = dp.getGamesWithPredicate(PPlayer(P.FIRST).HAS(PHero(Hero.Hunter))
#                               .AND(PNoMirrorDeck())
#                               .AND(PValid())
#                               .AND(PNot(PDraws()))
#                               .AND(PPlayer(P.SECOND).HAS(PHero(Hero.Mage))))
# print(len(g0))
# g1 = dp.getGamesWithPredicate(  PPlayer(P.FIRST).HAS(PHero(Hero.Hunter))
#                                 .OR(
#                                 PPlayer(P.SECOND).HAS(PHero(Hero.Hunter))).AND(PNoMirrorHero()))
# g2 = dp.getGamesWithPredicate(  PPlayer(P.FIRST).HAS(PHero(Hero.Hunter)).AND(PNoMirrorHero()))
# g3 = dp.getGamesWithPredicate(  PPlayer(P.SECOND).HAS(PHero(Hero.Hunter)).AND(PNoMirrorHero()))
# print(len(g1), ' ', len(g2), ' ', len(g3))
# print(len(dp.games))
# # g0 = dp.getGamesWithPredicate(PNot(PHero(Hero.Warlock)).AND(
# #                               PNot(PHero(Hero.Mage))).AND(
# #                               PNot(PHero(Hero.Druid))).AND(
# #                               PNot(PHero(Hero.Paladin))).AND(
# #                               PNot(PHero(Hero.Priest))).AND(
# #                               PNot(PHero(Hero.Rogue))).AND(
# #                               PNot(PHero(Hero.Shaman))).AND(
# #                               PNot(PHero(Hero.Warrior))))
#
# a = 1