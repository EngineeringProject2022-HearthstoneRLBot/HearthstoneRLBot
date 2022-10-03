import datetime
import glob
import os
import pickle

from pandas import DataFrame

from GameInterface.GameData import PlayerDecks
from GameFiles.DataProvider import DataProvider
import pandas as pd

class ExcelGenerator:

    def __init__(self, data_provider:DataProvider):
        self.data_provider = data_provider
        self.cols = {'Player1Name','Player1Deck','Player2Name','Winner','NumberOfTurns','StartPlayer','SecondPlayer','FileName'}

    def generateExcelForGame(self,game,fileName,index):

        self.CreateDirectoryIfMissing(path = f'data/ExcelFiles/SingleGames')

        df = pd.DataFrame({
        'Player1Name': game[3][0],
        'Player1Deck': self.mapDeckToDeckName(game[3][2]),
        'Player2Name': game[3][3],
        'Player2Deck': self.mapDeckToDeckName(game[3][5]),
        'First': game[3][6],
        'Second': game[3][7],
        'Winner': game[1],
        'NumberOfTurns': len(game[0]),
        'FileName': f'{fileName}.xlsx',
        'Traceback': "" if game[4] is None else game[4]
        },index=[0])

        writer = pd.ExcelWriter(f'data/ExcelFiles/SingleGames/{fileName}-{index}.xlsx')
        df.to_excel(writer)
        writer.save()
        print(f"Saved {fileName}.xlsx")

    def CreateDirectoryIfMissing(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    def mergeExcels(self):
        baseExcel = None
        pathToDirectory = f'data/ExcelFiles/MergedExcels'
        self.CreateDirectoryIfMissing(path=f'data/ExcelFiles/MergedExcels')
        for filepath in glob.iglob(f'data/ExcelFiles/SingleGames/*'):
            if baseExcel is None:
                baseExcelFilename = pathToDirectory + "/" +filepath.split("\\")[-1]
                baseExcel = pd.read_excel(filepath)
                continue
            nextExcel = pd.read_excel(filepath,engine="openpyxl")
            baseExcel = self.mergeTwoExcels(baseExcel,nextExcel,baseFilepath=baseExcelFilename)


    def mergeTwoExcels(self,df1,df2,baseFilepath):
        df1 = df1.append(df2)
        df1.to_excel(baseFilepath,index=[0])
        return df1

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

