import glob
import os
import pickle

import Configuration
from GameFiles.DataProvider import DataProvider
from GameInterface.GameData import PlayerDecks
import pandas as pd

class ExcelGenerator:

    def __init__(self):
        self.files = [filepath for filepath in glob.iglob(f'./data/{Configuration.OUTPUT_FOLDER}/*')]
        self.cols = {'Player1Name','Player1Deck','Player2Name','Winner','NumberOfTurns','StartPlayer','SecondPlayer','FileName'}

    def append_to_csv(self, game, fileName):

        self.create_missing_dir(path ='./data/ExcelFiles/SingleGames')
        self.create_blank_csv(filepath=f'./data/ExcelFiles/SingleGames/{fileName}.csv')
        df = pd.DataFrame({
        'Player1Name': game[3][0],
        'Player1Deck': self.map_deck_to_deck_name(game[3][2]),
        'Player2Name': game[3][3],
        'Player2Deck': self.map_deck_to_deck_name(game[3][5]),
        'First': game[3][6],
        'Second': game[3][7],
        'Winner': game[1],
        'NumberOfTurns': len(game[0]),
        'FileName': f'{fileName}',
        'Traceback': "" if game[4] is None else game[4]
        },index=[0])

        df.to_csv(f'./data/ExcelFiles/SingleGames/{fileName}.csv', mode='a', index=False,header=False)

    def create_blank_csv(self, filepath, merge=False):
        if not os.path.exists(filepath):
            df = pd.DataFrame(columns=['Player1Name','Player1Deck','Player2Name','Player2Deck','First','Second','Winner','NumberOfTurns','FileName','Traceback'])
            if not merge:
                df.to_csv(filepath,index_label=False,header=True)
            else:
                df.to_csv(filepath,index_label=False,header=True)

    def create_missing_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def merge_csv_files(self):
        resultCSV = f'data/ExcelFiles/MergedExcels/result.csv'
        self.create_blank_csv(filepath = resultCSV, merge=True)
        filenames = glob.iglob(f'data/ExcelFiles/SingleGames/*')
        with open(resultCSV, "a+") as target:
            for filename in filenames :
                with open(filename, "r") as f:
                    next(f)
                    for line in f:
                        target.write(line)

    def map_deck_to_deck_name(self, deck):
        for key in PlayerDecks.decks:
            if PlayerDecks.decks[key] == deck:
                return key

    def generate_game_csv_from_txt(self):
        for filepath in self.files:
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
                        tmp_path = filepath.replace('\\','/').split('/')
                        self.append_to_csv(game, tmp_path[-1])
                except EOFError:
                    print(f"EOF {filepath}")

