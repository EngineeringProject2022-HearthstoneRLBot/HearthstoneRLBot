import numpy as np
from tensorflow import keras
import Configuration
from GameFiles.DataProvider import BalanceType


class DataGenerator(keras.utils.Sequence):
    def __init__(self, batch_size=32, dim=(401, 41, 3), n_channels=1, shuffle=True):
        self.dp = Configuration.DATA_PROVIDER
        self.dim = dim
        self.batch_size = batch_size

        if Configuration.REMOVE_ONE_CHOICE_TURNS:
            filter_end_turns = True
        else:
            filter_end_turns = False

        if not Configuration.BALANCED_GAMES:
            balance_type = BalanceType.UNBALANCED
        else:
            if Configuration.BALANCED_BY_MATCHUP:
                balance_type = BalanceType.BALANCED_MATCHUPS
            else:
                balance_type = BalanceType.BALANCED_DECKS
        self.list_IDs = self.dp.validIds(filter_end_turns, balance_type)
        self.n_channels = n_channels
        self.shuffle = shuffle
        self.on_epoch_end()
        self.wvFunc = lambda turn: turn.pRef.winner - turn.pRef.loser
        self.probFunc = lambda turn: turn.probs

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

    def set_wv_func(self, func):
        self.wvFunc = func

    def set_prob_func(self, func):
        self.probFunc = func

    def __data_generation(self, listIdsTmp: []):
        X = []
        yValue = []
        yPolicy = []

        for id in listIdsTmp:
            try:
                turn = self.dp.turn(id)
                X.append(turn.sparseData.todense())
                yPolicy.append(self.probFunc(turn))
                yValue.append(self.wvFunc(turn))
            except Exception:
                print(listIdsTmp)
        return np.asarray(X).squeeze(1), [np.asarray(yPolicy), np.asarray(yValue)]
