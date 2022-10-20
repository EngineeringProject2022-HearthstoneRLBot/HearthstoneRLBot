from GameInterface import *
from collections import OrderedDict


class GameCreator:

    @staticmethod
    def drawRandomDeck(hero = None):
        if hero is None:
            randomDeck = random.choice(HeroDecks.AllDecks)
        else:
            randomDeck = random.choice(HeroDecks.HeroDeck(hero))
        return randomDeck

    @staticmethod
    def createDefaultGame(typep1=PlayerType.Modeled, typep2=None, modelp1="Model-INIT", modelp2=None,
                          simulationsp1=10, simulationsp2=None, p1=None, p2=None, printLogs=False):
        if typep2 is None:
            typep2 = typep1
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

        if typep1 == PlayerType.Random:
            name1 = '1' + nameDeckOne + '_' + 'Random'
            p1 = RandomPlayer(name1, heroDeckOne, deck1, printLogs)
        elif typep1 == PlayerType.Modeled:
            name1 = '1' + nameDeckOne + '_' + modelp1 + '_' + 'simulations' + str(simulationsp1)
            p1 = AIPlayer(name1, heroDeckOne, deck1, modelp1, simulationsp1)

        if typep2 == PlayerType.Random:
            name2 = '2' + nameDeckTwo + '_' + 'Random'
            p2 = RandomPlayer(name2, heroDeckTwo, deck2, printLogs)
        elif typep2 == PlayerType.Modeled:
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
    def createHunterTestGame(typep1=PlayerType.Modeled, typep2=None, modelp1="Model-INIT", modelp2=None):
        if typep2 is None:
            typep2 = typep1
        if modelp2 is None:
            modelp2 = modelp1
        game = GameCreator.createDefaultGame(typep1=typep1, typep2=typep2, modelp1=modelp1, modelp2=modelp2,
                                             p1=("HUNTER_TEST", Hero.Hunter, PlayerDecks.BasicHunter), p2=("HUNTER_TEST", Hero.Hunter, PlayerDecks.BasicHunter))
        startGameEffs = [GESetMaxMana(10), GEDealDmg(28), GEEndTurn(), GERemoveDeck(), GEDiscard()]
        startTurnEffs = [GEDiscard()]
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    @staticmethod
    def createFireballTest(typep1=PlayerType.Modeled, typep2=None, modelp1="Model-INIT", modelp2=None):
        if typep2 is None:
            typep2 = typep1
        if modelp2 is None:
            modelp2 = modelp1

        game = GameCreator.createDefaultGame(typep1=typep1, typep2=typep2, modelp1=modelp1, modelp2=modelp2,
                                             p1=("FIREBALL_TEST", Hero.Mage, PlayerDecks.BasicMage), p2=("FIREBALL_TEST", Hero.Mage, PlayerDecks.BasicMage))
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(24), GEPlayMinionTimes([('CS2_231', 7)]), GEEndTurn(), GERemoveDeck(), GEDiscard(), GEGiveCards([], [('CS2_029', 1)])]
        startTurnEffs = []
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    @staticmethod
    def createWeaponTest(typep1=PlayerType.Modeled, typep2=None, modelp1="Model-INIT", modelp2=None):
        if typep2 is None:
            typep2 = typep1
        if modelp2 is None:
            modelp2 = modelp1

        game = GameCreator.createDefaultGame(typep1=typep1, typep2=typep2, modelp1=modelp1, modelp2=modelp2,
                                             p1=("WEAPON_TEST", Hero.Warlock, PlayerDecks.BasicWarlock), p2=("WEAPON_TEST", Hero.Warlock, PlayerDecks.BasicWarlock))
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(27, 29), GEPlayMinionTimes([('CS2_231', 7)]), GEEndTurn(), GERemoveDeck(), GEDiscard(), GEPlayMinionTimes([('CS2_106', 1)])]
        startTurnEffs = []
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    @staticmethod
    def createDruidTestGame(typep1=PlayerType.Modeled, typep2=None, modelp1="Model-INIT", modelp2=None):
        if typep2 is None:
            typep2 = typep1
        if modelp2 is None:
            modelp2 = modelp1
        game = GameCreator.createDefaultGame(typep1=typep1, typep2=typep2, modelp1=modelp1, modelp2=modelp2,
                                             p1=("DRUID_TEST", Hero.Druid, PlayerDecks.BasicDruid), p2=("DRUID_TEST", Hero.Druid, PlayerDecks.BasicDruid))
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(29), GEEndTurn(), GERemoveDeck(), GEDiscard()]
        startTurnEffs = [GEDiscard()]
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    @staticmethod
    def createMageTestGame(typep1=PlayerType.Modeled, typep2=None, modelp1="Model-INIT", modelp2=None):
        if typep2 is None:
            typep2 = typep1
        if modelp2 is None:
            modelp2 = modelp1
        game = GameCreator.createDefaultGame(typep1=typep1, typep2=typep2, modelp1=modelp1, modelp2=modelp2,
                                             p1=("MAGE_TEST", Hero.Mage, PlayerDecks.BasicMage), p2=("MAGE_TEST", Hero.Mage, PlayerDecks.BasicMage))
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(29), GEEndTurn(), GERemoveDeck(), GEDiscard()]
        startTurnEffs = [GEDiscard()]
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    #5/2 and 2/3 vs. 3/5 taunt
    @staticmethod
    def createSmartTradeTest(typep1=PlayerType.Modeled, typep2=None, modelp1="Model-INIT", modelp2=None):
        if typep2 is None:
            typep2 = typep1
        if modelp2 is None:
            modelp2 = modelp1
        game = GameCreator.createDefaultGame(typep1=typep1, typep2=typep2, modelp1=modelp1, modelp2=modelp2,
                                             p1=("SMART_TRADE_TEST", Hero.Warlock, PlayerDecks.BasicWarlock), p2=("SMART_TRADE_TEST", Hero.Warlock, PlayerDecks.BasicWarlock))
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(29), GEPlayMinionTimes([('CS2_213', 1), ('CS2_120', 1)]), GEEndTurn(), GEPlayMinionTimes([('CS2_179', 1)]), GEEndTurn(), GERemoveDeck(), GEDiscard()]
        startTurnEffs = [GEDiscard()]
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    @staticmethod
    def createWindfuryWeaponTest(typep1=PlayerType.Modeled, typep2=None, modelp1="Model-INIT", modelp2=None):
        if typep2 is None:
            typep2 = typep1
        if modelp2 is None:
            modelp2 = modelp1
        game = GameCreator.createDefaultGame(typep1=typep1, typep2=typep2, modelp1=modelp1, modelp2=modelp2,
                                             p1=("WINDFURY_WEAPON_TEST", Hero.Warlock, PlayerDecks.BasicWarlock), p2=("WINDFURY_WEAPON_TEST", Hero.Warlock, PlayerDecks.BasicWarlock))
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(26), GEPlayMinionTimes([('CS2_231', 7)]), GEEndTurn(), GEPlayMinionTimes([('EX1_567', 1)]), GERemoveDeck(), GEDiscard()]
        startTurnEffs = [GEDiscard()]
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    @staticmethod
    def createLeperGnomeTest(typep1=PlayerType.Modeled, typep2=None, modelp1="Model-INIT", modelp2=None):
        if typep2 is None:
            typep2 = typep1
        if modelp2 is None:
            modelp2 = modelp1
        game = GameCreator.createDefaultGame(typep1=typep1, typep2=typep2, modelp1=modelp1, modelp2=modelp2,
                                             p1=("LEPERGNOME_TEST", Hero.Mage, PlayerDecks.BasicMage), p2=("LEPERGNOME_TEST", Hero.Hunter, PlayerDecks.BasicHunter))
        startGameEffs = [GESetStarterPlayer(1), GESetMaxMana(10), GEDealDmg(28, 26), GEPlayMinionTimes([('EX1_029', 1)]), GEEndTurn(), GEEndTurn(), GERemoveDeck(), GEDiscard()]
        startTurnEffs = [GEDiscard()]
        game.startGameEffs = startGameEffs
        game.startTurnEffs = startTurnEffs
        return game

    @staticmethod
    def createCustomGame():
        return Configuration.CUSTOM_GAME()