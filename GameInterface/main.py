from fireplace import cards
from GameInterface.AIPlayer import AIPlayer
from GameInterface.DiscardingGame import DiscardingGame
from GameInterface.ManualPlayer import ManualPlayer
from GameInterface.ModeledGame import ModeledGame
from GameInterface.RandomPlayer import RandomPlayer
from GameCreator import GameCreator
from GameCreator import HeroDecks
from GameCreator import PlayerType


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

def main():
    cards.db.initialize()
    game = GameCreator.createDefaultGame(player1Type=PlayerType.Modeled, modelp1="XYZ") #both players on the same model: XYZ
    game.start()


if __name__ == "__main__":
    main()
