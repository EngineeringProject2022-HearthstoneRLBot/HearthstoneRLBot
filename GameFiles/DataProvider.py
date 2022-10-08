import glob
import pickle
import types
import numpy as np
import sparse


class DataProvider:
    def __init__(self,data_folder):
        self.data_folder=data_folder
        self.data = []
        self.initData()
        self.total_no_turns = len(self.data)

    def initData(self):
        return self.iterateFilesAndGames(self.__getInfoForGames)

    def iterateFilesAndGames(self,*args):
        fun = None
        for arg in args:
            if isinstance(arg,types.MethodType) or isinstance(arg,types.FunctionType):
                fun = arg
        if fun is None:
            return
        for filepath in glob.iglob(f'data/{self.data_folder}/*'):
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
                        fun(game,winner,args)
                except EOFError:
                    print(f"EOF {filepath}")

    def __getInfoForGames(self, game, winner, *args):
        singleGameTurns = len(game[0])
        for turnNo in range(singleGameTurns):
            if game[0][turnNo][2] == winner:
                value = 1
            elif game[0][turnNo][2] < 3:
                value = -1
            else:
                value = 0

            X = sparse.COO(np.asarray(game[0][turnNo][0]))
            Y = [np.asarray(game[0][turnNo][1]),np.asarray(value)]
            self.data.append([X,Y])



