import glob
import pickle
from typing.io import BinaryIO
import numpy as np
import sparse


class DataProvider:

    def __init__(self,directory_path:str):
        self.directory_path = directory_path

    def getWinners(self) -> []:
        winners = []
        for filepath in glob.iglob(f'{self.directory_path}/*'):
            with open(filepath,"rb") as file_stream:
                try:
                    pickle.load(file_stream)
                    while True:
                        game = pickle.load(file_stream)
                        winner = game[1]
                        if winner > 3:
                            continue
                        winners.append(winner)
                except EOFError:
                    print("EOF")
        return winners

    def getCombinedTuplesOfDecks(self) -> []:
        decks = []
        for filepath in glob.iglob(f'{self.directory_path}/*'):
            with open(filepath,"rb") as file_stream:
                decks = self.__getDecksFromOneFile(decks, file_stream)
        return decks

    def __getDecksFromOneFile(self,decks,file_stream:BinaryIO) -> []:
        try:
            pickle.load(file_stream)
            while True:
                game = pickle.load(file_stream)
                winner = game[1]
                if winner > 3:
                    continue
                decks.append((game[0][0][1],game[0][0][3])) # xd
        except EOFError:
            print("EOF")
        return decks

    def getCombinedNumberOfTurns(self) -> []:
        noTurns = []
        for filepath in glob.iglob(f'{self.directory_path}/*'):
            with open(filepath,"rb") as file_stream:
                noTurns += self.__getNumberOfTurns(file_stream)
        return noTurns

    def getCombinedNumberOfGames(self) -> int:
        return self.__getTotalNumber(self.__getNumberOfGames)

    def __getTotalNumber(self,func,total):
        for filepath in glob.iglob(f'{self.directory_path}/*'):
            with open(filepath,"rb") as file_stream:
                total += func(file_stream)
        return total

    def __mergeDictionaries(self,x:{}, y:{}) -> {}:
        z:{} = x.copy()
        z.update(y)
        return z

    def getCombinedTurnsDictionary(self):
        turns_dictionary = {}
        next_key = 1
        for filepath in glob.iglob(f'{self.directory_path}/*'):
            with open(filepath,"rb") as file_stream:
                single_game_dict,next_key = self.__getTurnsDictionary(next_key=next_key,file_stream=file_stream)

                turns_dictionary = self.__mergeDictionaries(turns_dictionary,single_game_dict)

        return turns_dictionary

    def __getTurnsDictionary(self,next_key:int,file_stream:BinaryIO):
        game_dictionary = {}
        try:
            pickle.load(file_stream)
            while True:
                game = pickle.load(file_stream)
                winner = game[1]
                if winner > 3:
                    continue
                single_game_turns = len(game[0])
                for turnNo in range(1,single_game_turns,1):
                    if game[0][turnNo][2] == winner:
                        value = 1
                    elif game[0][turnNo][2] < 3:
                        value = -1
                    else:
                        value = 0
                    game_dictionary[next_key] = [sparse.COO(np.asarray(game[0][turnNo][0])), [np.asarray(game[0][turnNo][1]),np.asarray(value)]]
                    next_key += 1
        except EOFError:
            return game_dictionary, next_key


        return game_dictionary, next_key

    def __getNumberOfTurns(self,file_stream:BinaryIO) -> []:
        turns = []
        try:
            pickle.load(file_stream)
            while True:
                game = pickle.load(file_stream)
                winner = game[1]
                if winner > 3:
                    continue
                turns.append(len(game[0]) - 1 )

        except EOFError:
            print("EOF")

        return turns

    def __getNumberOfGames(self,file_stream:BinaryIO) -> int:
        games_count = 0
        try:
            pickle.load(file_stream)
            while True:
                game = pickle.load(file_stream)
                winner = game[1]
                if winner > 3:
                    continue
                games_count += 1
        except EOFError:
            print("EOF")

        return games_count



