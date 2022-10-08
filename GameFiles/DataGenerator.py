import glob
import pickle

import numpy as np
import sparse
from tensorflow import keras

from GameFiles.DataProvider import DataProvider


class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'

    def __init__(self, data_folder, batch_size=32, dim=(401, 41, 3), n_channels=1, shuffle=True):
        'Initialization'
        self.__data_provider = DataProvider(data_folder)
        self.dim = dim
        self.batch_size = batch_size
        self.data = self.getData()
        self.no_turns = self.getNoTurns()
        self.list_IDs = [*range(0, self.no_turns)]
        self.n_channels = n_channels
        self.shuffle = shuffle
        self.on_epoch_end()

    def getData(self):
        return self.__data_provider.data

    def getNoTurns(self):
        return self.__data_provider.total_no_turns

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]

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

    # Zakladam ze lista ID bedzie miala najmniejszy mozliwy element == 1, zeby nie sprawdzac pierwszej tury gdzie jest deck. W razie co mozna po prostu dodac 1 do indeksu i po problemie :D
    def __data_generation(self, listIdsTmp: []):
        X = []
        yValue = []
        yPolicy = []

        for id in listIdsTmp:
            try:
                X.append(self.data[id][0].todense())
                yPolicy.append(self.data[id][1][0])
                yValue.append(self.data[id][1][1])
            except Exception:
                print(listIdsTmp)
        return np.asarray(X).squeeze(1), [np.asarray(yPolicy), np.asarray(yValue)]
