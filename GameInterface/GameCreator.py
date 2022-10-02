from GameInterface import *


class GameCreator:

    @staticmethod
    def drawRandomDeck():
        randomDeck = random.choice(HeroDecks.AllDecks)
        return randomDeck


    @staticmethod
    def createDefaultGame(player1Type=PlayerType.Modeled, player2Type=None, modelp1="Model-INIT", modelp2=None,
                          depthp1=10, depthp2=None, p1=None, p2=None, printLogs=False):
        if player2Type is None:
            player2Type = player1Type
        if depthp2 is None:
            depthp2 = depthp1
        if modelp2 is None:
            modelp2 = modelp1
        if p1 is None:
            p1 = GameCreator.drawRandomDeck()
        if p2 is None:
            p2 = GameCreator.drawRandomDeck()
        nameDeckOne, heroDeckOne, deck1 = p1
        nameDeckTwo, heroDeckTwo, deck2 = p2

        #solving same decks and player types
        if nameDeckOne == nameDeckTwo and player1Type == player2Type and modelp1 == modelp2 and depthp1 == depthp2:
            nameDeckOne = nameDeckOne + "1"
            nameDeckTwo = nameDeckTwo + "2"

        if player1Type == PlayerType.Random:
            name1 = nameDeckOne + '_' + 'Random'
            p1 = RandomPlayer(name1, heroDeckOne, deck1, printLogs)
        elif player1Type == PlayerType.Modeled:
            name1 = nameDeckOne + '_' + modelp1 + '_' + 'depth' + str(depthp1)
            p1 = AIPlayer(name1, heroDeckOne, deck1, modelp1, depthp1)

        if player2Type == PlayerType.Random:
            name2 = nameDeckTwo + '_' + 'Random'
            p2 = RandomPlayer(name2, heroDeckTwo, deck2, printLogs)
        elif player2Type == PlayerType.Modeled:
            name2 = nameDeckTwo + '_' + modelp2 + '_' + 'depth' + str(depthp2)
            p2 = AIPlayer(name2, heroDeckTwo, deck2, modelp2, depthp2)

        game = DecoratedGame(p1, p2)
        return game

    @staticmethod
    def createDefaultModelGame(model="Model-INIT", depth=20, p1=None, p2=None):
        if p1 is None:
            p1 = GameCreator.drawRandomDeck()
        if p2 is None:
            p2 = GameCreator.drawRandomDeck()
        nameDeckOne, heroDeckOne, deck1 = p1
        nameDeckTwo, heroDeckTwo, deck2 = p2
        name1 = nameDeckOne + '_' + model + '_' + 'depth' + str(depth)
        name2 = nameDeckTwo + '_' + model + '_' + 'depth' + str(depth)
        p1 = AIPlayer(name1, heroDeckOne, deck1, model, depth)
        p2 = AIPlayer(name2, heroDeckTwo, deck2, model, depth)
        game = ModeledGame(p1, p2)
        return game

    @staticmethod
    def createDefaultRandomGame(printLogs=False, p1=None, p2=None):
        if p1 is None:
            p1 = GameCreator.drawRandomDeck()
        if p2 is None:
            p2 = GameCreator.drawRandomDeck()
        nameDeckOne, heroDeckOne, deck1 = p1
        nameDeckTwo, heroDeckTwo, deck2 = p2
        name1 = nameDeckOne + '_' + 'Random'
        name2 = nameDeckTwo + '_' + 'Random'
        p1 = RandomPlayer(name1, heroDeckOne, deck1, printLogs)
        p2 = RandomPlayer(name2, heroDeckTwo, deck2, printLogs)
        game = ModeledGame(p1, p2)
        return game

    @staticmethod
    def createHunterTestGame(player1Type=PlayerType.Modeled, player2Type=None, modelp1="Model-INIT", modelp2=None):
        if player2Type is None:
            player2Type = player1Type
        if modelp2 is None:
            modelp2 = modelp1
        game = GameCreator.createDefaultGame(player1Type=player1Type, player2Type=player2Type, modelp1=modelp1, modelp2=modelp2,
                                             p1=("HUNTER_TEST", Hero.Hunter, PlayerDecks.BasicHunter), p2=("HUNTER_TEST", Hero.Hunter, PlayerDecks.BasicHunter))
        startGameEffs = [GESetMana(10), GEDealDmg(28), GEEndTurn(), GERemoveDeck(), GEDiscard()]
        startTurnEffs = [GEDiscard()]
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    # @staticmethod
    # def testGiveAndPlay(player1Type=PlayerType.Random, player2Type=None, modelp1="Model-INIT", modelp2=None):
    #     if player2Type is None:
    #         player2Type = player1Type
    #     if modelp2 is None:
    #         modelp2 = modelp1
    #     game = GameCreator.createDefaultGame(player1Type=player1Type, player2Type=player2Type, modelp1=modelp1, modelp2=modelp2,
    #                                          p1=("TMP", Hero.Hunter, PlayerDecks.BasicHunter), p2=("TMP", Hero.Rogue, PlayerDecks.BasicHunter))
    #     startGameEffs = [GESetMana(10), GEDealDmg(28), GEGiveAndPlayMinions(['CS2_231', 'CS2_231']), GERemoveDeck(), GEDiscard()]
    #     startTurnEffs = [GEDiscard()]
    #     game.startGameEffs = startGameEffs
    #     game.startTurnEffs = startTurnEffs
    #     return game

    @staticmethod
    def createCustomGame():
        return Configuration.CUSTOM_GAME()