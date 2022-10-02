import glob
import pickle

import numpy as np
from tensorflow import keras
import sparse


class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'

    def __init__(self, data_folder, batch_size=32, dim=(401, 41, 3), n_channels=1, shuffle=True):
        'Initialization'
        self.data_folder = data_folder
        self.dim = dim
        self.batch_size = batch_size
        self.dictionary = {}
        self.list_IDs = [*range(1, self.__getNoTurns__() + 1)]
        self.n_channels = n_channels
        self.shuffle = shuffle
        self.on_epoch_end()

    def __getNoTurns__(self):
        noTurns = 0

        for filepath in glob.iglob(f'../data/{self.data_folder}/*'):
            with open(filepath, "rb") as rb:
                # METADATA AND DECK TO BE IGNORED
                try:
                    # SKIP METADATA
                    pickle.load(rb)
                    while True:
                        game = pickle.load(rb)
                        winner = game[1]
                        if winner > 3:
                            continue
                        singleGameTurns = len(game[0])

                        for turnNo in range(1, singleGameTurns, 1):
                            if game[0][turnNo][2] == winner:
                                value = 1
                            elif game[0][turnNo][2] < 3:
                                value = -1
                            else:
                                value = 0

                            self.dictionary[len(self.dictionary) + 1] = [sparse.COO(np.asarray(game[0][turnNo][0])),
                                                                         [np.asarray(game[0][turnNo][1]),
                                                                          np.asarray(value)]]

                except EOFError:
                    print(f"EOF {filepath}")

        return len(self.dictionary)

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
                X.append(self.dictionary[id][0].todense())
                yPolicy.append(self.dictionary[id][1][0])
                yValue.append(self.dictionary[id][1][1])
            except:
                print(listIdsTmp)
        return np.asarray(X).squeeze(1), [np.asarray(yPolicy), np.asarray(yValue)]
