from GameInterface import *

# MonteCarlo
WIN_MULTIPLIER = 1
RANDOM_MOVE_SAMPLES = 5

# DumpGames
OUTPUT_FOLDER = 'DEFAULT_OUTPUT'
GAME_NUM = 200

# Training
INPUT_MODEL_NAME = 'Model-Init'
OUTPUT_MODEL_NAME = 'exp'
LEARNING_RATE = 0.00001
DATA_FOLDER = "rand_data_1"
POLICY_WEIGHT = 1
WINVALUE_WEIGHT = 1
#set to 0 to disable
CALLBACKS = 1
CALLBACK_FREQ = 2000

# Game creation
def GAME_CREATION():
    return GameCreator.createDefaultGame(typep1=PlayerType.Modeled, p1=HeroDecks.BasicHunter, modelp1='19200games')
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