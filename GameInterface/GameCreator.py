from GameInterface import *
from collections import OrderedDict


class GameCreator:

    @staticmethod
    def drawRandomDeck():
        randomDeck = random.choice(HeroDecks.AllDecks)
        return randomDeck


    @staticmethod
    def createDefaultGame(player1Type=PlayerType.Modeled, player2Type=None, modelp1="Model-INIT", modelp2=None,
                          simulationsp1=10, simulationsp2=None, p1=None, p2=None, printLogs=False):
        if player2Type is None:
            player2Type = player1Type
        if simulationsp2 is None:
            simulationsp2 = simulationsp1
        if modelp2 is None:
            modelp2 = modelp1
        if p1 is None:
            p1 = GameCreator.drawRandomDeck()
        if p2 is None:
            p2 = GameCreator.drawRandomDeck()
        nameDeckOne, heroDeckOne, deck1 = p1
        nameDeckTwo, heroDeckTwo, deck2 = p2

        if player1Type == PlayerType.Random:
            name1 = '1' + nameDeckOne + '_' + 'Random'
            p1 = RandomPlayer(name1, heroDeckOne, deck1, printLogs)
        elif player1Type == PlayerType.Modeled:
            name1 = '1' + nameDeckOne + '_' + modelp1 + '_' + 'simulations' + str(simulationsp1)
            p1 = AIPlayer(name1, heroDeckOne, deck1, modelp1, simulationsp1)

        if player2Type == PlayerType.Random:
            name2 = '2' + nameDeckTwo + '_' + 'Random'
            p2 = RandomPlayer(name2, heroDeckTwo, deck2, printLogs)
        elif player2Type == PlayerType.Modeled:
            name2 = '2' + nameDeckTwo + '_' + modelp2 + '_' + 'simulations' + str(simulationsp2)
            p2 = AIPlayer(name2, heroDeckTwo, deck2, modelp2, simulationsp2)

        game = DecoratedGame(p1, p2)
        return game

    @staticmethod
    def createDefaultModelGame(model="Model-INIT", simulations=20, p1=None, p2=None):
        if p1 is None:
            p1 = GameCreator.drawRandomDeck()
        if p2 is None:
            p2 = GameCreator.drawRandomDeck()
        nameDeckOne, heroDeckOne, deck1 = p1
        nameDeckTwo, heroDeckTwo, deck2 = p2
        name1 = nameDeckOne + '_' + model + '_' + 'simulations' + str(simulations)
        name2 = nameDeckTwo + '_' + model + '_' + 'simulations' + str(simulations)
        p1 = AIPlayer(name1, heroDeckOne, deck1, model, simulations)
        p2 = AIPlayer(name2, heroDeckTwo, deck2, model, simulations)
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
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(28), GEEndTurn(), GERemoveDeck(), GEDiscard()]
        startTurnEffs = [GEDiscard()]
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    @staticmethod
    def createFireballTest(player1Type=PlayerType.Modeled, player2Type=None, modelp1="Model-INIT", modelp2=None):
        if player2Type is None:
            player2Type = player1Type
        if modelp2 is None:
            modelp2 = modelp1

        game = GameCreator.createDefaultGame(player1Type=player1Type, player2Type=player2Type, modelp1=modelp1, modelp2=modelp2,
                                             p1=("FIREBALL_TEST", Hero.Mage, PlayerDecks.BasicMage), p2=("FIREBALL_TEST", Hero.Mage, PlayerDecks.BasicMage))
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(24), GEPlayMinionTimes([('CS2_231', 7)]), GEEndTurn(), GERemoveDeck(), GEDiscard(), GEGiveCards([], [('CS2_029', 1)])]
        startTurnEffs = []
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    @staticmethod
    def createWeaponTest(player1Type=PlayerType.Modeled, player2Type=None, modelp1="Model-INIT", modelp2=None):
        if player2Type is None:
            player2Type = player1Type
        if modelp2 is None:
            modelp2 = modelp1

        game = GameCreator.createDefaultGame(player1Type=player1Type, player2Type=player2Type, modelp1=modelp1, modelp2=modelp2,
                                             p1=("WEAPON_TEST", Hero.Warlock, PlayerDecks.BasicWarlock), p2=("WEAPON_TEST", Hero.Warlock, PlayerDecks.BasicWarlock))
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(27, 29), GEPlayMinionTimes([('CS2_231', 7)]), GEEndTurn(), GERemoveDeck(), GEDiscard(), GEPlayMinionTimes([('CS2_106', 1)])]
        startTurnEffs = []
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game


    @staticmethod
    def createCustomGame():
        return Configuration.CUSTOM_GAME()