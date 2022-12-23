from GameFiles.DataProvider import DataProvider
from GameInterface.GameCreator import *
from tensorboard.plugins.hparams import api as hp

# Threads
NUM_THREADS = 6

# MonteCarlo
WIN_MULTIPLIER = 1
RANDOM_MOVE_SAMPLES = 5
MCTS_CHILD_MULTIPLIER = 2

# DumpGames
OUTPUT_FOLDER = 'DEFAULT_OUTPUT'
GAME_NUM = 1

# Training
INPUT_MODEL_NAME = 'Model-TEST'
OUTPUT_MODEL_NAME = 'dnnB_05'
OPTIMIZER = hp.HParam('optimizer', hp.Discrete(['adam', 'sgd']))
LEARNING_RATE = hp.HParam('learning_rate')
POLICY_WEIGHT = hp.HParam('policy_weight', hp.RealInterval(0.0, 1.0))
WINVALUE_WEIGHT = hp.HParam('winvalue_weight', hp.RealInterval(0.0, 1.0))
BATCH_SIZE = hp.HParam("batch_size", hp.IntInterval(1, 64))
HPARAMS = [
    OPTIMIZER,
    LEARNING_RATE,
    POLICY_WEIGHT,
    WINVALUE_WEIGHT,
    BATCH_SIZE
]

#METRIC_RMSE = 'RootMeanSquaredError'
METRIC_ACCURACY = 'accuracy'

hparams = {
    OPTIMIZER: "adam",
    LEARNING_RATE: 1e-6,
    POLICY_WEIGHT: 1,
    WINVALUE_WEIGHT: 1,
    BATCH_SIZE: 1
}

# LEARNING_RATE = 0.00001
#Provide correct filepath to excel files directory if different
#CSV_PROVIDER = DataProvider.CSVFromFolder("ExcelFiles/SingleGames")
DATA_PROVIDER = DataProvider.DataFromFolder("dnn")
# POLICY_WEIGHT = 1
# WINVALUE_WEIGHT = 1

LOG_TREE = False # change this value in training.py

BALANCED_GAMES = False
BALANCED_BY_MATCHUP = False
REMOVE_ONE_CHOICE_TURNS = False
# BATCH_SIZE = 1

#set to 0 to disable
CALLBACKS = 1
CALLBACK_FREQ = 2000



# Game creation
def GAME_CREATION():
    return GameCreator.createDefaultGame(PlayerType.Modeled,
                                         #p1 = GameCreator.drawRandomDeck('OilRogue'),
                                         #p2 = GameCreator.drawRandomDeck('MurlocPaladin'),
                                         modelp1='dnnB_1',
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
