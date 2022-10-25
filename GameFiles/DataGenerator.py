import numpy as np
from tensorflow import keras
import Configuration


class DataGenerator(keras.utils.Sequence):
    def __init__(self, batch_size=32, dim=(401, 41, 3), n_channels=1, shuffle=True):
        self.dp = Configuration.DATA_PROVIDER
        self.dim = dim
        self.batch_size = batch_size
        self.list_IDs = self.dp.balancedIds() if Configuration.BALANCED_GAMES else self.dp.validIds()
        self.n_channels = n_channels
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        list_IDs_temp = [self.list_IDs[k] for k in indexes]
        X, y = self.__data_generation(list_IDs_temp)
        return X, y

    def on_epoch_end(self):
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, listIdsTmp: []):
        X = []
        yValue = []
        yPolicy = []

        for id in listIdsTmp:
            try:
                turn = self.dp.turn(id)
                X.append(turn.sparseData.todense())
                yPolicy.append(turn.probs)
                yValue.append(turn.pRef.winner-turn.pRef.loser)
            except Exception:
                print(listIdsTmp)
        return np.asarray(X).squeeze(1), [np.asarray(yPolicy), np.asarray(yValue)]
