import pandas as pd
import numpy as np

def setHeroesForData(df):
    df['Player1Hero'] = ""
    df['Player2Hero'] = ""
    decks = ["Player1Deck", "Player2Deck"]
    heroes = ["Player1Hero", "Player2Hero"]
    for i in range(0, 2):
        # Druid filter
        df.loc[(df[decks[i]] == 'BasicDruid') | (df[decks[i]] == 'MidrangeDruid') | (
                    df[decks[i]] == 'FastDruid'), [heroes[i]]] = 'Druid'
        # Hunter filter
        df.loc[(df[decks[i]] == 'BasicHunter') | (df[decks[i]] == 'AgroHunter') | (
                    df[decks[i]] == 'FaceHunter'), [heroes[i]]] = 'Hunter'
        # Mage filter
        df.loc[(df[decks[i]] == 'BasicMage') | (df[decks[i]] == 'MechMage') | (
                    df[decks[i]] == 'FlamewalkerTempoMage'), [heroes[i]]] = 'Mage'
        # Paladin filter
        df.loc[(df[decks[i]] == 'BasicPaladin') | (df[decks[i]] == 'ControlPaladin') | (
                    df[decks[i]] == 'MurlocPaladin'), [heroes[i]]] = 'Paladin'
        # Priest filter
        df.loc[(df[decks[i]] == 'BasicPriest') | (df[decks[i]] == 'ControlPriest') | (
                    df[decks[i]] == 'DragonPriest'), [heroes[i]]] = 'Priest'
        # Rogue filter
        df.loc[(df[decks[i]] == 'BasicRogue') | (df[decks[i]] == 'OilRogue'), [heroes[i]]] = 'Rogue'
        # Shaman filter
        df.loc[(df[decks[i]] == 'BasicShaman') | (df[decks[i]] == 'MidrangeShaman'), [heroes[i]]] = 'Shaman'
        # Warlock filter
        df.loc[(df[decks[i]] == 'BasicWarlock') | (df[decks[i]] == 'DemonZoo') | (df[decks[i]] == 'DemonZooWarlock'), [heroes[i]]] = 'Warlock'
        # Warrior filter
        df.loc[
            (df[decks[i]] == 'BasicWarrior') | (df[decks[i]] == 'MidrangeWarrior'), [heroes[i]]] = 'Warrior'

        df.loc[(df[decks[i]] == 'DemonZoo'), [decks[i]]] = 'DemonZooWarlock'
    return df

def getWinrateForDeck(data, deckName):
    players = ['Player1Deck', 'Player2Deck']
    playerNames = ['Player1Name', 'Player2Name']
    relevantWinNumber = 0
    relevantLossNumber = 0
    turns = 0

    for i in range(0, 2):
        tmp = data.loc[(data[players[i]] == deckName)]
        tmp = tmp.loc[(tmp['Winner'] == 1) | (tmp['Winner'] == 2)]
        tmp['Loser'] = ""
        tmp['relevantWon'] = ""
        tmp['relevantLost'] = ""
        tmp.loc[(tmp['Winner'] == 1), ['Loser']] = tmp['Second']
        tmp.loc[(tmp['Winner'] == 2), ['Loser']] = tmp['First']

        tmp.loc[(tmp['Winner'] == 1), ['Winner']] = tmp['First']
        tmp.loc[(tmp['Winner'] == 2), ['Winner']] = tmp['Second']

        tmp.loc[(tmp['Winner'] == tmp[playerNames[i]]), ['relevantWon']] = 1
        tmp.loc[(tmp['Winner'] != tmp[playerNames[i]]), ['relevantWon']] = 0

        tmp.loc[(tmp['Loser'] == tmp[playerNames[i]]), ['relevantLost']] = 1
        tmp.loc[(tmp['Loser'] != tmp[playerNames[i]]), ['relevantLost']] = 0

        relevantWinNumber += tmp['relevantWon'].sum()
        relevantLossNumber += tmp['relevantLost'].sum()
        turns += tmp['NumberOfTurns'].sum()
    return (relevantWinNumber + relevantLossNumber), relevantWinNumber, relevantLossNumber, (turns/(relevantWinNumber + relevantLossNumber))

def getWinrateForDeckFirst(data, deckName):
    players = ['Player1Deck', 'Player2Deck']
    playerNames = ['Player1Name', 'Player2Name']
    relevantWinNumber = 0
    relevantLossNumber = 0
    games = 0

    for i in range(0, 2):
        tmp = data.loc[(data[players[i]] == deckName)]
        tmp = tmp.loc[(tmp['Winner'] == 1) | (tmp['Winner'] == 2)]
        tmp = tmp.loc[(tmp[playerNames[i]] == tmp['First'])]
        tmp['Loser'] = ""
        tmp['relevantWon'] = ""
        tmp['relevantLost'] = ""
        tmp.loc[(tmp['Winner'] == 1), ['Loser']] = tmp['Second']
        tmp.loc[(tmp['Winner'] == 2), ['Loser']] = tmp['First']

        tmp.loc[(tmp['Winner'] == 1), ['Winner']] = tmp['First']
        tmp.loc[(tmp['Winner'] == 2), ['Winner']] = tmp['Second']

        tmp.loc[(tmp['Winner'] == tmp["First"]), ['relevantWon']] = 1
        tmp.loc[(tmp['Winner'] != tmp["First"]), ['relevantWon']] = 0

        tmp.loc[(tmp['Loser'] == tmp["First"]), ['relevantLost']] = 1
        tmp.loc[(tmp['Loser'] != tmp["First"]), ['relevantLost']] = 0

        relevantWinNumber += tmp['relevantWon'].sum()
        relevantLossNumber += tmp['relevantLost'].sum()
        games += tmp['First'].count()
    return games, relevantWinNumber, relevantLossNumber

def getWinrateForDeckSecond(data, deckName):
    players = ['Player1Deck', 'Player2Deck']
    playerNames = ['Player1Name', 'Player2Name']
    relevantWinNumber = 0
    relevantLossNumber = 0
    games = 0

    for i in range(0, 2):
        tmp = data.loc[(data[players[i]] == deckName)]
        tmp = tmp.loc[(tmp['Winner'] == 1) | (tmp['Winner'] == 2)]
        tmp = tmp.loc[(tmp[playerNames[i]] == tmp['Second'])]
        tmp['Loser'] = ""
        tmp['relevantWon'] = ""
        tmp['relevantLost'] = ""
        tmp.loc[(tmp['Winner'] == 1), ['Loser']] = tmp['Second']
        tmp.loc[(tmp['Winner'] == 2), ['Loser']] = tmp['First']

        tmp.loc[(tmp['Winner'] == 1), ['Winner']] = tmp['First']
        tmp.loc[(tmp['Winner'] == 2), ['Winner']] = tmp['Second']

        tmp.loc[(tmp['Winner'] == tmp["Second"]), ['relevantWon']] = 1
        tmp.loc[(tmp['Winner'] != tmp["Second"]), ['relevantWon']] = 0

        tmp.loc[(tmp['Loser'] == tmp["Second"]), ['relevantLost']] = 1
        tmp.loc[(tmp['Loser'] != tmp["Second"]), ['relevantLost']] = 0

        relevantWinNumber += tmp['relevantWon'].sum()
        relevantLossNumber += tmp['relevantLost'].sum()
        games += tmp['Second'].count()
    return games, relevantWinNumber, relevantLossNumber

def getWinrateForHero(data, heroName):
    heroes = ['Player1Hero', 'Player2Hero']
    playerNames = ['Player1Name', 'Player2Name']
    relevantWinNumber = 0
    relevantLossNumber = 0
    turns = 0

    for i in range(0, 2):
        tmp = data.loc[(data[heroes[i]] == heroName)]
        tmp = tmp.loc[(tmp['Winner'] == 1) | (tmp['Winner'] == 2)]
        tmp['Loser'] = ""
        tmp['relevantWon'] = ""
        tmp['relevantLost'] = ""
        tmp.loc[(tmp['Winner'] == 1), ['Loser']] = tmp['Second']
        tmp.loc[(tmp['Winner'] == 2), ['Loser']] = tmp['First']

        tmp.loc[(tmp['Winner'] == 1), ['Winner']] = tmp['First']
        tmp.loc[(tmp['Winner'] == 2), ['Winner']] = tmp['Second']

        tmp.loc[(tmp['Winner'] == tmp[playerNames[i]]), ['relevantWon']] = 1
        tmp.loc[(tmp['Winner'] != tmp[playerNames[i]]), ['relevantWon']] = 0

        tmp.loc[(tmp['Loser'] == tmp[playerNames[i]]), ['relevantLost']] = 1
        tmp.loc[(tmp['Loser'] != tmp[playerNames[i]]), ['relevantLost']] = 0

        relevantWinNumber += tmp['relevantWon'].sum()
        relevantLossNumber += tmp['relevantLost'].sum()
        turns += tmp['NumberOfTurns'].sum()
    return (relevantWinNumber + relevantLossNumber), relevantWinNumber, relevantLossNumber, (turns/(relevantWinNumber + relevantLossNumber))

def getWinrateForHeroFirst(data, heroName):
    heroes = ['Player1Hero', 'Player2Hero']
    playerNames = ['Player1Name', 'Player2Name']
    relevantWinNumber = 0
    relevantLossNumber = 0
    games = 0

    for i in range(0, 2):
        tmp = data.loc[(data[heroes[i]] == heroName)]
        tmp = tmp.loc[(tmp['Winner'] == 1) | (tmp['Winner'] == 2)]
        tmp = tmp.loc[(tmp[playerNames[i]] == tmp['First'])]
        tmp['Loser'] = ""
        tmp['relevantWon'] = ""
        tmp['relevantLost'] = ""
        tmp.loc[(tmp['Winner'] == 1), ['Loser']] = tmp['Second']
        tmp.loc[(tmp['Winner'] == 2), ['Loser']] = tmp['First']

        tmp.loc[(tmp['Winner'] == 1), ['Winner']] = tmp['First']
        tmp.loc[(tmp['Winner'] == 2), ['Winner']] = tmp['Second']

        tmp.loc[(tmp['Winner'] == tmp["First"]), ['relevantWon']] = 1
        tmp.loc[(tmp['Winner'] != tmp["First"]), ['relevantWon']] = 0

        tmp.loc[(tmp['Loser'] == tmp["First"]), ['relevantLost']] = 1
        tmp.loc[(tmp['Loser'] != tmp["First"]), ['relevantLost']] = 0

        relevantWinNumber += tmp['relevantWon'].sum()
        relevantLossNumber += tmp['relevantLost'].sum()
        games += tmp['First'].count()
    return games, relevantWinNumber, relevantLossNumber

def getWinrateForHeroSecond(data, heroName):
    heroes = ['Player1Hero', 'Player2Hero']
    playerNames = ['Player1Name', 'Player2Name']
    relevantWinNumber = 0
    relevantLossNumber = 0
    games = 0

    for i in range(0, 2):
        tmp = data.loc[(data[heroes[i]] == heroName)]
        tmp = tmp.loc[(tmp['Winner'] == 1) | (tmp['Winner'] == 2)]
        tmp = tmp.loc[(tmp[playerNames[i]] == tmp['Second'])]
        tmp['Loser'] = ""
        tmp['relevantWon'] = ""
        tmp['relevantLost'] = ""
        tmp.loc[(tmp['Winner'] == 1), ['Loser']] = tmp['Second']
        tmp.loc[(tmp['Winner'] == 2), ['Loser']] = tmp['First']

        tmp.loc[(tmp['Winner'] == 1), ['Winner']] = tmp['First']
        tmp.loc[(tmp['Winner'] == 2), ['Winner']] = tmp['Second']

        tmp.loc[(tmp['Winner'] == tmp["Second"]), ['relevantWon']] = 1
        tmp.loc[(tmp['Winner'] != tmp["Second"]), ['relevantWon']] = 0

        tmp.loc[(tmp['Loser'] == tmp["Second"]), ['relevantLost']] = 1
        tmp.loc[(tmp['Loser'] != tmp["Second"]), ['relevantLost']] = 0

        relevantWinNumber += tmp['relevantWon'].sum()
        relevantLossNumber += tmp['relevantLost'].sum()
        games += tmp['Second'].count()
    return games, relevantWinNumber, relevantLossNumber

def getWinrateForFirst(data):
    tmp = data.loc[(data['Winner'] == 1) | (data['Winner'] == 2)]
    tmp.loc[(tmp['Winner'] == 1), ['Loser']] = tmp['Second']
    tmp.loc[(tmp['Winner'] == 2), ['Loser']] = tmp['First']
    tmp.loc[(tmp['Winner'] == 1), ['Winner']] = tmp['First']
    tmp.loc[(tmp['Winner'] == 2), ['Winner']] = tmp['Second']
    tmp = tmp.loc[(tmp['First'] == tmp['Winner'])]

    wins = tmp['Winner'].count()
    total = data['Winner'].count()
    return wins, total

def getWinrateForSecond(data):
    tmp = data.loc[(data['Winner'] == 1) | (data['Winner'] == 2)]
    tmp.loc[(tmp['Winner'] == 1), ['Loser']] = tmp['Second']
    tmp.loc[(tmp['Winner'] == 2), ['Loser']] = tmp['First']
    tmp.loc[(tmp['Winner'] == 1), ['Winner']] = tmp['First']
    tmp.loc[(tmp['Winner'] == 2), ['Winner']] = tmp['Second']
    tmp = tmp.loc[(tmp['Second'] == tmp['Winner'])]

    wins = tmp['Winner'].count()
    total = data['Winner'].count()
    return wins, total

decks = ['BasicDruid', 'BasicHunter', 'BasicMage', 'BasicPaladin', 'BasicPriest', 'BasicRogue', 'BasicShaman', 'BasicWarlock',
         'BasicWarrior', 'MidrangeDruid', 'AgroHunter', 'MechMage', 'ControlPaladin', 'ControlPriest', 'OilRogue', 'MidrangeShaman',
         'DemonZooWarlock', 'MidrangeWarrior', 'FastDruid', 'FaceHunter', 'FlamewalkerTempoMage', 'MurlocPaladin', 'DragonPriest']
heroes = ['Druid', 'Hunter', 'Mage', 'Paladin', 'Priest', 'Rogue', 'Shaman', 'Warlock', 'Warrior']
dfDeck = pd.DataFrame()
dfHero = pd.DataFrame()

tmp = pd.read_csv('G:/HearthstoneRLBot/data/ExcelFiles/MergedExcels/result.csv')
# tmp = pd.read_csv('G:/HearthstoneRLBot/data/ExcelFiles/SingleGames/18-10-2022T165247.csv')
# tmp = pd.read_csv('G:/PobraneG/model_result_200games.csv')
# tmp = pd.read_csv('G:/PobraneG/wojtek_test.csv')
newTMP = tmp[['Player1Name', 'Player2Name', 'Player1Deck', 'Player2Deck', 'First', 'Second', 'Winner', 'NumberOfTurns', 'Traceback']]
newTMP = setHeroesForData(newTMP)

gamesPlayed = []
Winrate = []
averageTurns = []
gamesPlayedFirst = []
winrateFirst = []
gamesPlayedSecond = []
winrateSecond = []

for deck in decks:
    a = getWinrateForDeck(newTMP, deck)
    gamesPlayed.append(a[0])
    Winrate.append(a[1]/a[0])
    averageTurns.append(a[3])

    a = getWinrateForDeckFirst(newTMP, deck)
    gamesPlayedFirst.append(a[0])
    winrateFirst.append(a[1] / a[0])

    a = getWinrateForDeckSecond(newTMP, deck)
    gamesPlayedSecond.append(a[0])
    winrateSecond.append(a[1] / a[0])

dfDeck['DeckName'] = decks
dfDeck['GamesPlayed'] = gamesPlayed
dfDeck['Winrate'] = Winrate
dfDeck['GamesPlayedFirst'] = gamesPlayedFirst
dfDeck['WinrateFirst'] = winrateFirst
dfDeck['GamesPlayedSecond'] = gamesPlayedSecond
dfDeck['WinrateSecond'] = winrateSecond
dfDeck['AverageTurns'] = averageTurns

# -------------------------------------------------------------------------------------------------------------------- #
gamesPlayed = []
Winrate = []
averageTurns = []
gamesPlayedFirst = []
winrateFirst = []
gamesPlayedSecond = []
winrateSecond = []

for hero in heroes:
    a = getWinrateForHero(newTMP, hero)
    gamesPlayed.append(a[0])
    Winrate.append(a[1]/a[0])
    averageTurns.append(a[3])

    a = getWinrateForHeroFirst(newTMP, hero)
    gamesPlayedFirst.append(a[0])
    winrateFirst.append(a[1] / a[0])

    a = getWinrateForHeroSecond(newTMP, hero)
    gamesPlayedSecond.append(a[0])
    winrateSecond.append(a[1] / a[0])

dfHero['Hero'] = heroes
dfHero['GamesPlayed'] = gamesPlayed
dfHero['Winrate'] = Winrate
dfHero['GamesPlayedFirst'] = gamesPlayedFirst
dfHero['WinrateFirst'] = winrateFirst
dfHero['GamesPlayedSecond'] = gamesPlayedSecond
dfHero['WinrateSecond'] = winrateSecond
dfHero['AverageTurns'] = averageTurns



dfDeck = dfDeck.sort_values(by=['Winrate'], ascending=False)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(dfDeck)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     print(dfHero)

# a = (dfDeck['GamesPlayedFirst']*dfDeck['WinrateFirst'] + dfDeck['GamesPlayedSecond']*dfDeck['WinrateSecond'])/(dfDeck['GamesPlayed'].sum())
# a = dfDeck['GamesPlayed']*dfDeck['Winrate']
# print(a.sum())
# print(a.sum())






# print(getWinrateForDeck(newTMP, 'DemonZooWarlock'))
# print(getWinrateForDeckFirst(newTMP, 'DemonZooWarlock'))
# print(getWinrateForDeckSecond(newTMP, 'DemonZooWarlock'))
#
# print(newTMP['NumberOfTurns'].mean())
# print(getWinrateForHero(newTMP, 'Warlock'))
# print(getWinrateForHeroFirst(newTMP, 'Warlock'))
# print(getWinrateForHeroSecond(newTMP, 'Warlock'))
#
# print(getWinrateForFirst(newTMP))
# print(getWinrateForSecond(newTMP))