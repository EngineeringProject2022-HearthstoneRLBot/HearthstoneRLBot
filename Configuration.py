from GameFiles.DataProvider import DataProvider
from GameInterface.GameCreator import *

# Threads
NUM_THREADS = 6

# MonteCarlo
WIN_MULTIPLIER = 1
RANDOM_MOVE_SAMPLES = 5
MCTS_CHILD_MULTIPLIER = 2

# DumpGames
OUTPUT_FOLDER = 'DEFAULT_OUTPUT'
GAME_NUM = 2000

# Training
INPUT_MODEL_NAME = 'ckpt-loss=1.10'
OUTPUT_MODEL_NAME = 'exp'
LEARNING_RATE = 0.00001
#Provide correct filepath to excel files directory if different
#CSV_PROVIDER = DataProvider.CSVFromFolder("ExcelFiles/SingleGames")
DATA_PROVIDER = DataProvider.DataFromFolder("DEFAULT_OUTPUT")
POLICY_WEIGHT = 0.2
WINVALUE_WEIGHT = 1
BALANCED_GAMES = True
BALANCED_BY_DECK = True
BATCH_SIZE = 1
#set to 0 to disable
CALLBACKS = 1
CALLBACK_FREQ = 2000

# Game creation
def GAME_CREATION():
    return GameCreator.createDefaultGame(PlayerType.Modeled,
                                         #p1 = GameCreator.drawRandomDeck('OilRogue'),
                                         #p2 = GameCreator.drawRandomDeck('MurlocPaladin'),
                                         modelp1='Model-TEST',
                                         simulationsp1 = 50)
    #return GameCreator.createCustomGame()

def CUSTOM_GAME():
    p1 = RandomPlayer("HUNTER_TEST", Hero.Hunter, PlayerDecks.BasicHunter)
    p2 = RandomPlayer("HUNTER_TEST", Hero.Hunter, PlayerDecks.BasicHunter)
    startGameEffs = [GESetMana(10), GEDealDmg(28), GEEndTurn(), GERemoveDeck(), GEDiscard()]
    startTurnEffs = [GEDiscard()]
    game = DecoratedGame(p1, p2,
                         startGameEffs=startGameEffs,
                         startTurnEffs=startTurnEffs)
    return game


# GameCreator.createDefaultGame() user Manual:
# Arguments:
# player1/2Type --> type of player (ex.Random/Modeled) if you pass only player1Type then player2Type will be the same
# modelp1/p2    --> model that player will use,        if you pass only modelp1 then the players will use the same model
# depthp1/p2    --> number of simulations in the tree, if you pass only depthp1 then the players will have the same depth
# p1/p2         --> basically decks for players that we can give manually, use HeroDecks. ... and just choose the deck USE "()" p1=()
# createDefaultGame(playerType=PlayerType.Random)  - Basic random vs random moves on randomly picked decks
# createDefaultGame(playerType=PlayerType.Modeled) - Basic model  vs model  moves on randomly picked decks
# createDefaultGame(player1Type=PlayerType.Modeled, modelp1="NAZWA_MODELU", depthp1=25) #both players on same model->NAZWA_MODELU and on the same depth=25
# createDefaultGame(player1Type=PlayerType.Modeled, modelp1="NAZWA_MODELU", depthp1=25 ,p1=(HeroDecks.BasicDruid), player2Type=PlayerType.Random, p2=(HeroDecks.FastDruid), printLogs=True)
# createCustomGame() zwraca CUSTOM_GAME z konfiguracji ( to jest miejsce jeżeli się chce dodać własny test i go popróbować )


# dp = DATA_PROVIDER
# from GameFiles.DataPredicates import *
# games = dp.getGamesWithPredicate(
#     PPlayer(P.FIRST).HAS(PDeck('BasicHunter').WINS())
#                                  .AND(
#     PPlayer(P.SECOND).HAS(PDeck('BasicMage'))))
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
