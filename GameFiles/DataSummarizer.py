
from HearthstoneRLBot.DataProvider import DataProvider
import pandas as pd

class DataSummarizer:

    def __init__(self, data_provider:DataProvider):
        self.data_provider = data_provider

    def generateExcelStatistics(self):
        winners = self.data_provider.getWinners()
        decks = self.data_provider.getCombinedTuplesOfDecks()
        numbers_of_turns = self.data_provider.getCombinedNumberOfTurns()


        # cols = {
        #             ''
        #             'Winners':winners,
        #             'NumberOfTurns':numbers_of_turns
        #            }
        # columns = {'Player1Name',
        #            'Player1Deck',
        #            'Player2Name',
        #            'Player2Deck',
        #            'NumberOfTurns',
        #            'Winner',
        #            'FileName'
        #            }
        # data_frame = pd.DataFrame(data=cols)
        # data_frame.to_excel(f"summary.xlsx")

