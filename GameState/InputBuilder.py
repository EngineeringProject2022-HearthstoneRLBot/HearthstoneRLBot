from GameState import HandCards
from GameState import Hero
import numpy as np
from numpy import array

class InputBuilder:

    def HandFunction(listOfCardsOnHand):
        counter = 0
        playerHandDecode = []
        for i in range(0,10):
            counter = len(listOfCardsOnHand)
            Res = np.zeros((39,39))
            if(i < counter):
                test = HandCards.HandCard(listOfCardsOnHand[i])
                Res = test.encode_state()
            playerHandDecode.append(Res)
        finalPlayerHand = np.hstack((playerHandDecode[0:]))
       # finalPlayerHand = np.c_[np.zeros(41), finalPlayerHand]
        return finalPlayerHand

    def BoardFunction(listOfCardsOnBoard, listOfHeroFeatures):
        counter = 0
        playerBoardDecode = []
        for i in range(0,7):
            counter = len(listOfCardsOnBoard)
            Res = np.zeros((39,39))
            if(i < counter):
                test = HandCards.HandCard(listOfCardsOnBoard[i])
                Res = test.encode_state()
            playerBoardDecode.append(Res)
        #APPEND HERO FEATURES

        for elem in listOfHeroFeatures:
            playerBoardDecode.append(elem)
        #playerBoardDecode.append(listOfHeroFeatures[0:])
        finalPlayerBoard = np.hstack((playerBoardDecode[0:]))
 #       finalPlayerBoard =  np.c_[np.zeros(41), finalPlayerBoard]
        return finalPlayerBoard

    @staticmethod
    def convToInput(game, player_perspective=None):
        if player_perspective is None:
            player_perspective = game.current_player
        elif player_perspective == 1:
            player_perspective = game.player1
        elif player_perspective == 2:
            player_perspective = game.player2
        else:
            raise Exception

        p1 = player_perspective
        p2 = p1.opponent
        # if simulatingPlayer == 1:
        #     p1 = game.player1
        #     p2 = game.player2
        # elif simulatingPlayer == 2:
        #     p1 = game.player2
        #     p2 = game.player1

        player1Hand = p1.hand
        player2Hand = p2.hand
        # currPlayer = game.current_player
        boardPlayer1 = p1.field #game.board #albo field
        boardPlayer2 = p2.field
        
        tmp1 = Hero.Hero()
        tmp2 = Hero.Hero()
        hero1 = p1.hero
        hero2 = p2.hero
        hero1st = tmp1.HeroDecode(hero1)
        hero2nd = tmp2.HeroDecode(hero2)
        res1 = tmp1.encode_state(hero1st)
        res2 = tmp2.encode_state(hero2nd)

        FP1Hand = InputBuilder.HandFunction(player1Hand)
        #FP2Hand = InputBuilder.HandFunction(player2Hand)

        FP1Board = InputBuilder.BoardFunction(boardPlayer1, res1)
        FP2Board = InputBuilder.BoardFunction(boardPlayer2, res2)

        if player_perspective == game.current_player:
            playerArr = np.zeros((117, 390))
        elif player_perspective == game.current_player.opponent:
            playerArr = np.ones((117, 390))
        else:
            raise Exception
        # remove opp hand?
        MegaFinalMatrix = np.concatenate((FP2Board,FP1Board,FP1Hand
        #                        FP2Hand,
                                 #playerArr
                                 ))
        #MegaFinalMatrix = np.array([MegaFinalMatrix,playerArr])
        # x y z order
        MegaFinalMatrix = MegaFinalMatrix[None, :]
        MegaFinalMatrix = np.moveaxis(MegaFinalMatrix,[0],[2])
        # dummy dimension needed for model
        MegaFinalMatrix = MegaFinalMatrix[None, :]
        return MegaFinalMatrix

#Symulujacy to 0 i 1 to on, dalej 2 3 przeciwnik i potem currentPlayer Matrix