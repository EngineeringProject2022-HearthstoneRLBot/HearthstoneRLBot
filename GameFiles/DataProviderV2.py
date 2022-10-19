import glob
import pickle
import random
from GameInterface import HeroDecks


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
    def __init__(self, id, gameElement, turnCnt):
        self.id = id
        self.turnCnt = turnCnt
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
            turns.append(self.analyzeTurnElement(self.turnCnt + len(turns), turnElement, p1, p2))
        return p1, p2, winner, turns, traceback

    def analyzeTurnElement(self, id, turnElement, p1, p2):
        input = turnElement[0]
        policy = turnElement[1]
        player = turnElement[2]
        action = turnElement[3]
        return STurn(id, input, policy, action, p1 if player == 1 else p2)


class DataProvider:
    def __init__(self, files):
        self.games = []
        self.turns = []
        for filepath in files:
            with open(filepath, "rb") as rb:
                try:
                    # SKIP METADATA
                    pickle.load(rb)
                    while True:
                        game = pickle.load(rb)
                        sGame = SGame(len(self.games), game, len(self.turns))
                        self.turns.extend(sGame.turns)
                        self.games.append(sGame)
                except EOFError:
                    print(f"EOF {filepath}")

    def getGamesWithWinnerValue(self,value):
        return [game for game in self.games if game.winner == value]

    def getFirstGamesForEachClass(self,game_count):
        gamesForClass = []
        for hero in range(2,10):
            gamesForClass.extend(self.getFirstXGamesForClass(hero,game_count))
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

    # self.games
    # game -> id, p1, p2, turns, winner(1,2,3,4)
    # player -> hero, deck, simulations, model, wins=True/False, loses=True/False, game
    # turn -> id, p1/p2, data, action, ...
    # self.deckname, self.hero, self.modelname, self.simulations = self.parseName(name)
    # self.winner = winner
    # self.loser = loser
    # self.game = game

    def balancedIds(self):
        counter = {}
        indices = []
        noTurns = []
        balanced_turns = {}
        
        for id, turn in enumerate(self.turns):
            player = turn.pRef
            if not player.deckname in counter:
                counter[player.deckname] = [0, 0, [],[]]
            if player.winner:
                counter[player.deckname][0] += 1
                counter[player.deckname][2].append(turn)
            if player.loser:
                counter[player.deckname][1] += 1
                counter[player.deckname][3].append(turn)

        for deck in counter.keys():
            noTurns.append(counter[deck][0])
            noTurns.append(counter[deck][1])
            
        globalMin = min(noTurns)

        for cnt in counter:
            if cnt not in balanced_turns:
                balanced_turns[cnt] = [[],[]]
            balanced_turns[cnt][0] = random.sample(counter[cnt][2],globalMin)
            balanced_turns[cnt][1] = random.sample(counter[cnt][3],globalMin)

        for cnt in balanced_turns.values():
            indices.extend([turn.id for turn in cnt[0]])
            indices.extend([turn.id for turn in cnt[1]])

        return indices

    @staticmethod
    def DataFromFolder(folder):
        return DataProvider([filepath for filepath in glob.iglob(f'../data/{folder}/*')])

    @staticmethod
    def CSVFromFolder(folder):
        pass

    @staticmethod
    def DataFromFile(file):
        return DataProvider([f'../data/{file}'])

    @staticmethod
    def CSVFromFile(file):
        pass



#dp = DataProvider.DataFromFolder('DEFAULT_OUTPUT')
#x = dp.getGamesWithWinnerValue(2)
#d = dp.balancedIds()
#f = dp.getFirstGamesForEachClass(50)
#print("yolo")