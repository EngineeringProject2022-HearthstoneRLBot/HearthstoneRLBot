import glob
import os
import pickle
from GameInterface.GameData import PlayerDecks
import pandas as pd

class ExcelGenerator:

    def __init__(self):
        self.cols = {'Player1Name','Player1Deck','Player2Name','Winner','NumberOfTurns','StartPlayer','SecondPlayer','FileName'}

    def AppendGameToExcel(self,game,fileName):

        self.CreateDirectoryIfMissing(path = 'data/ExcelFiles/SingleGames')
        self.CreateBlankCsv(filepath= f'data/ExcelFiles/SingleGames/{fileName}.csv')
        df = pd.DataFrame({
        'Player1Name': game[3][0],
        'Player1Deck': self.mapDeckToDeckName(game[3][2]),
        'Player2Name': game[3][3],
        'Player2Deck': self.mapDeckToDeckName(game[3][5]),
        'First': game[3][6],
        'Second': game[3][7],
        'Winner': game[1],
        'NumberOfTurns': len(game[0]),
        'FileName': f'{fileName}',
        'Traceback': "" if game[4] is None else game[4]
        },index=[0])

        df.to_csv(f'data/ExcelFiles/SingleGames/{fileName}.csv', mode='a', index=False,header=False)

    def CreateBlankCsv(self,filepath,merge=False):
        if not os.path.exists(filepath):
            df = pd.DataFrame(columns=['Player1Name','Player1Deck','Player2Name','Player2Deck','First','Second','Winner','NumberOfTurns','FileName','Traceback'])
            if not merge:
                df.to_csv(filepath,header=True)
            else:
                df.to_csv(filepath,header=True)

    def CreateDirectoryIfMissing(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    def Merge(self):
        resultCSV = f'data/ExcelFiles/MergedExcels/result.csv'
        self.CreateBlankCsv(filepath = resultCSV, merge=True)
        filenames = glob.iglob(f'data/ExcelFiles/SingleGames/*')
        with open(resultCSV, "a+") as target:
            for filename in filenames :
                with open(filename, "r") as f:
                    next(f)
                    for line in f:
                        target.write(line)

    def mapDeckToDeckName(self,deck):
        for key in PlayerDecks.decks:
            if PlayerDecks.decks[key] == deck:
                return key

    def generateExcelStatistics(self):
        for filepath in glob.iglob(f'{self.data_provider.directory_path}/*'):
            with open(filepath,"rb") as file_stream:
                try:
                    i = 0
                    x = pickle.load(file_stream)
                    while True:
                        i += 1
                        game = pickle.load(file_stream)
                        winner = game[1]
                        if winner > 3:
                            continue
                        tmp_path = filepath.replace('\\','/').split('/')
                        self.generateExcelForGame(game,tmp_path[-1],i)
                except EOFError:
                    print(f"Successfuly generated excels for {filepath}")

