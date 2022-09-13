import copy
import glob
import pickle

import numpy as np
import keras
from numpy import sort

GAME_INDEX = 0

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self,model_name, batch_size=32, dim=(401, 41, 3), n_channels=1, shuffle=True):
        'Initialization'
        self.model_name = model_name
        self.dim = dim
        self.batch_size = batch_size
        self.list_IDs = [*range(1,self.getNoTurns()+1)]
        self.n_channels = n_channels
        self.shuffle = shuffle
        self.on_epoch_end()

    def getNoTurns(self):
        noTurns = 0
        for filepath in glob.iglob(f'../data/{self.model_name}/*'):
            with open(filepath,"rb") as rb:
                #METADATA AND DECK TO BE IGNORED
                try:
                    #SKIP METADATA
                    pickle.load(rb)
                    while True:
                        game = pickle.load(rb)
                        noTurns += len(game[0])
                except EOFError:
                    break
        return noTurns

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

    # [ 5, 10 , 15, 20 ]
    # Zakladam ze lista ID bedzie miala najmniejszy mozliwy element == 1, zeby nie sprawdzac pierwszej tury gdzie jest deck. W razie co mozna po prostu dodac 1 do indeksu i po problemie :D
    def __data_generation(self,listIdsTmp:[]):#,listIds:[]):
        listIds = sort(listIdsTmp)
        X = []
        yValue = []
        yPolicy = []
        for filepath in glob.iglob(f'../data/{self.model_name}/*'):
            with open(filepath,"rb") as rb:
                try:
                    #SKIP METADATA
                    pickle.load(rb)
                    while True:

                            idsToRemove = []
                            game = pickle.load(rb)
                            winner = game[1]

                            for i,id in enumerate(listIds):
                                if id <= len(game[0]) - 1:
                                    if game[0][id][2] == winner:
                                        value = 1
                                    elif game[0][id][2] < 3:
                                        value = -1
                                    else:
                                        value = 0
                                    X.append(game[0][id][0])
                                    yPolicy.append(game[0][id][1])
                                    yValue.append(value)
                                    idsToRemove.append(i)
                                else:
                                    break

                            listIds = np.delete(listIds,idsToRemove)

                            if listIds.size == 0:
                                return np.asarray(X).squeeze(1), [np.asarray(yPolicy),np.asarray(yValue)]

                            listIds = [id - len(game[0]) + 1 for id in listIds]

                except EOFError:
                    break

        return np.asarray(X).squeeze(1), [np.asarray(yPolicy),np.asarray(yValue)]


    # def getGamesWithoutExceptionsFromSeveralFiles(numberOfGames: int):
    #     cleanGames = []
    #     global FILE_POSITION
    #     FILE_POSITION = 0
    #     for filepath in glob.iglob('data/Model-INIT/*'):
    #         gamesInFile = DataGenerator.getGamesWithoutExceptions(filepath,num_games=numberOfGames)
    #         if gamesInFile[0] == [] or gamesInFile[1] == []:
    #             continue
    #         cleanGames.append(gamesInFile)
    #     return cleanGames

    # def getGamesWithoutExceptions(filepath:str, num_games:int =50):
    #     global FILE_POSITION
    #     arrOfGames = []
    #     first_iteration = True
    #
    #     with open(filepath,"rb") as rb:
    #         while FILE_POSITION < num_games:
    #             try:
    #                 if first_iteration:
    #                     pickle.load(rb)
    #                     first_iteration = not first_iteration
    #                 elif FILE_POSITION <= num_games:
    #                     tmp = pickle.load(rb)
    #                     if not tmp:
    #                         FILE_POSITION -= 1
    #                         return
    #                     if tmp[1] < 4: # mniejsze od 4 to dozwolone stany gry ( nie wyjątki )
    #                         FILE_POSITION += 1
    #                         if FILE_POSITION >= num_games:
    #                             return arrOfGames
    #                         arrOfGames.append(tmp)
    #                     else:
    #                         FILE_POSITION -= 1
    #             except EOFError:
    #                 return arrOfGames
    #
    #         return arrOfGames

