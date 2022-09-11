import copy
import glob
import pickle

import numpy as np
import keras
from numpy import sort

GAME_INDEX = 0

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, batch_size=32, dim=(401, 41, 3), n_channels=1, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def getGamesWithoutExceptionsFromSeveralFiles(numberOfGames: int):
        cleanGames = []
        global FILE_POSITION
        FILE_POSITION = 0
        for filepath in glob.iglob('data/Model-INIT/*'):
            gamesInFile = DataGenerator.getGamesWithoutExceptions(filepath,num_games=numberOfGames)
            if gamesInFile[0] == [] or gamesInFile[1] == []:
                continue
            cleanGames.append(gamesInFile)
        return cleanGames

    def getGamesWithoutExceptions(filepath:str, num_games:int =50):
        global FILE_POSITION
        arrOfGames = []
        first_iteration = True

        with open(filepath,"rb") as rb:
            while FILE_POSITION < num_games:
                try:
                    if first_iteration:
                        pickle.load(rb)
                        first_iteration = not first_iteration
                    elif FILE_POSITION <= num_games:
                        tmp = pickle.load(rb)
                        if not tmp:
                            FILE_POSITION -= 1
                            return
                        if tmp[1] < 4: # mniejsze od 4 to dozwolone stany gry ( nie wyjątki )
                            FILE_POSITION += 1
                            if FILE_POSITION >= num_games:
                                return arrOfGames
                            arrOfGames.append(tmp)
                        else:
                            FILE_POSITION -= 1
                except EOFError:
                    return arrOfGames

            return arrOfGames

    def filter_list(L):
        return

    # [ 5, 10 , 15, 20 ]
    # Zakladam ze lista ID bedzie miala najmniejszy mozliwy element == 1, zeby nie sprawdzac pierwszej tury gdzie jest deck. W razie co mozna po prostu dodac 1 do indeksu i po problemie :D
    def getTurnsByIds(xyz = 0):#,listIds:[]):
        listIds = [1,3,5,120]
        idsToRemove = []
        maxID = max(listIds)
        turns = []
        next = False
        for filepath in glob.iglob('data/Model-INIT/*'):
            breakCondition = True
            with open(filepath,"rb") as rb:
                #METADATA AND DECK TO BE IGNORED
                metadata = pickle.load(rb)
                while True:
                    try:
                        for idRemove in idsToRemove:
                            if idRemove in listIds:
                                listIds.remove(idRemove)
                        if next:
                            listIds = [id - len(game[0]) + 1 for id in listIds]
                            next = False
                        game = pickle.load(rb)
                        for id in listIds:
                            winner = game[1]
                            if id <= len(game[0]) - 1:
                                if game[0][id][2] == winner:
                                    value = 1
                                elif game[0][id][2] < 3:
                                    value = -1
                                else:
                                    value = 0
                                turns.append((game[0][id][0],(game[0][id][1],value)))
                                idsToRemove.append(id)
                            else:
                                next = True
                                break
                    except EOFError:
                        break

        return turns


    def getNumberOfTurnsForOneGame(self):


        pass

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization


        # X = np.empty((self.batch_size, *self.dim, self.n_channels))
        # y = np.empty((self.batch_size), dtype=int)


        # for turn in game[0][1:]: # list of turns
        #     if type(turn) is not str:
        #         if winner < 3:
        #             input = turn[0]
        #             x.append(input)
        #             policy = turn[1]
        #             yPolicy.append(policy)
        #             if turn[2] == winner:
        #                 value = 1
        #             elif turn[2] < 3:
        #                 value = -1
        #             else:
        #                 value = 0
        #             yValue.append(value)


        # Generate data
        for i, ID in enumerate(list_IDs_temp): # potrzebujemy wybierać konkretne gry z danego pliku zamiast pliku
            # Store sample
            minID = min(list_IDs_temp)
            maxID = max(list_IDs_temp)
            # X[i,] = np.load('data/' + ID + '.txt')
            #
            # # Store class
            # y[i] = self.labels[ID]

        return X, y

