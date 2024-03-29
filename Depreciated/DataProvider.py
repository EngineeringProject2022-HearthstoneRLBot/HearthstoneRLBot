import glob
import pickle
import types
import numpy as np
import sparse

import Configuration


class DataProvider:
    def __init__(self,init_data = True):
        self.data_folder=Configuration.DATA_FOLDER
        self.data = []
        if init_data:
            self.initialize_data()
        self.total_no_turns = len(self.data)

    def initialize_data(self):
        return self.iterate_through_files(self.__get_info_for_games)

    def iterate_through_files(self, *args):
        fun = None
        for arg in args:
            if isinstance(arg,types.MethodType) or isinstance(arg,types.FunctionType):
                fun = arg
        if fun is None:
            return
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
                        fun(game,winner,filepath)
                except EOFError:
                    print(f"EOF {filepath}")

    def __get_info_for_games(self, *args):
        game = args[0]
        winner = args[1]
        singleGameTurns = len(game[0])
        for turnNo in range(singleGameTurns):
            if game[0][turnNo][2] == winner:
                value = 1
            elif game[0][turnNo][2] < 3:
                value = -1
            else:
                value = 0

            X = sparse.COO(np.asarray(game[0][turnNo][0])) # tutaj bez sparse bo bedzie zapisywane sparsowane
            Y = [np.asarray(game[0][turnNo][1]),np.asarray(value)]
            self.data.append([X,Y])



