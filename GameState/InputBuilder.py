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
            RES = np.zeros((41,40))
            if(i < counter):
                test = HandCards.HandCard(listOfCardsOnHand[i])
                RES = test.encode_state()
            playerHandDecode.append(RES)
        finalPlayerHand = np.hstack((playerHandDecode[0:]))
        finalPlayerHand =  np.c_[np.zeros(41), finalPlayerHand]
        return finalPlayerHand

    def BoardFunction(listOfCardsOnBoard, listOfHeroFeatures):
        counter = 0
        playerBoardDecode = []
        for i in range(0,7):
            counter = len(listOfCardsOnBoard)
            RES = np.zeros((41,40))
            if(i < counter):
                test = HandCards.HandCard(listOfCardsOnBoard[i])
                RES = test.encode_state()
            playerBoardDecode.append(RES)
        #APPEND HERO FEATURES

        for elem in listOfHeroFeatures:
            playerBoardDecode.append(elem)
        #playerBoardDecode.append(listOfHeroFeatures[0:])
        finalPlayerBoard = np.hstack((playerBoardDecode[0:]))
        finalPlayerBoard =  np.c_[np.zeros(41), finalPlayerBoard]
        return finalPlayerBoard

    def convToInput(game, simulatingPlayer):
        if simulatingPlayer == 1:
            p1 = game.player1
            p2 = game.player2
        elif simulatingPlayer == 2:
            p1 = game.player2
            p2 = game.player1

        player1Hand = p1.hand
        player2Hand = p2.hand
        currPlayer = game.current_player
        boardPlayer1 = p1.field #game.board #albo field
        boardPlayer2 = p2.field
        
        tmp1 = Hero.Hero()
        tmp2 = Hero.Hero()
        hero1 = p1.hero #player 1 i player 2 sa pozamieniane chyba####
        hero2 = p2.hero
        hero1st = tmp1.HeroDecode(hero1)
        hero2nd = tmp2.HeroDecode(hero2)
        res1 = tmp1.encode_state(hero1st)
        res2 = tmp2.encode_state(hero2nd)

        FP1Hand = InputBuilder.HandFunction(player1Hand) #Player 1 ktorym powinen byc rexxar jest Guldan czyli player2 w sumie!!!
        #FP2Hand = InputBuilder.HandFunction(player2Hand)

        FP1Board = InputBuilder.BoardFunction(boardPlayer1, res1)
        FP2Board = InputBuilder.BoardFunction(boardPlayer2, res2)

        if(str(currPlayer) == 'Player1'):
            playerArr = np.zeros((41,401))
        elif(str(currPlayer) == 'Player2'):
            playerArr = np.ones((41,401))
        # remove opp hand
        MegaFinalMatrix = array([FP1Hand, FP1Board, FP2Board,
        #                         FP2Hand,
                                 playerArr])
        # x y z order
        MegaFinalMatrix = np.moveaxis(MegaFinalMatrix,[1,2],[1,0])
        # dummy dimension needed for model
        MegaFinalMatrix = MegaFinalMatrix[None, :]
        return MegaFinalMatrix

#Symulujacy to 0 i 1 to on, dalej 2 3 przeciwnik i potem currentPlayer Matrix