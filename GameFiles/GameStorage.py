import os
import pickle
import glob
import random
import traceback

import sparse
import tensorflow as tf
import Configuration
import numpy as np

from GameFiles.ExcelGenerator import ExcelGenerator
from GameInterface.GameCreator import *
from datetime import datetime

excel_gen = ExcelGenerator()

def convert_to_sparse(game_output):
    y = []
    try:
        for x in game_output:
            y.append((sparse.COO(x[0]),x[1],x[2],x[3]))
        return y
    except Exception:
        print(traceback.format_exc())
        raise Exception

def dumpGames(output_folder = Configuration.OUTPUT_FOLDER):
    path = f"data/{output_folder}"
    if not os.path.exists(path):
        os.makedirs(path)
    fileName = datetime.now().strftime("%d-%m-%YT%H%M%S")
    with open(f"data/{output_folder}/{fileName}.txt", "wb") as fp:  # dumpuję aktualny(pierwszy) stan randoma jako pierwszy obiekt przed zrobieniem czegokolwiek
        pickle.dump((random.getstate()), fp)
        np.random.seed(random.randrange(999999999))
        tf.random.set_seed(random.randrange(999999999))

    for i in range(Configuration.GAME_NUM):
        print("GAME " + str(i + 1))
        state = random.getstate()
        game = Configuration.GAME_CREATION()
        output = None
        try:
            game.start()
            sparse_data = convert_to_sparse(game.data)
            output = (sparse_data, game.winner,   state, game.prepareGamersData(), None)
        except Exception:
            sparse_data = convert_to_sparse(game.data)
            output = (sparse_data, 4,             state, game.prepareGamersData(), traceback.format_exc())
            print(traceback.format_exc())
        with open(f"data/{output_folder}/{fileName}.txt", "ab") as fp:
            pickle.dump(output, fp)
        excel_gen.append_to_csv(game=output, fileName=fileName)



####FUNCTIONS TO CHECK (depreciated?)


# def selfPlay(model, numbgame, simulations, fileName, model_name, pureRand=False):
#     for i in range(numbgame):
#
#         print("GAME " + str(i + 1))
#         state = random.getstate()
#         game_player = GamePlayer(model, simulations)
#         if not pureRand:
#             winner, data = game_player.playGame()
#         else:
#             winner, data = game_player.playRandGame()
#         with open(f"data/{model_name}/{fileName}.txt", "ab") as fp:
#             pickle.dump((data, winner, state), fp)


def mostRecentFile():
    mostRecent = None
    mostRecentFilepath = None
    for filepath in glob.iglob('data/*'):
        x = filepath \
            .replace("data\\", "") \
            .replace(".txt", "")
        if not mostRecent:
            mostRecent = datetime.strptime(x,"%d-%m-%YT%H%M%S")
            mostRecentFilepath = x
            continue
        tmp = datetime.strptime(x,"%d-%m-%YT%H%M%S")
        if mostRecent <= tmp:
            mostRecentFilepath = x
            mostRecent = tmp


    return f"data\\{mostRecentFilepath}.txt"

def summarizeFile(filePath, comprehensive):
    if not comprehensive:
        games, firstWins, secondWins, draws, exceptions = fileStatistics(filePath)
        print('{} Games {} First {} Second {} Draws {} Exceptions {}'
              .format(filePath, games, firstWins, secondWins, draws, exceptions))
        return
    with open(filePath, "rb") as rb:
        metadata = pickle.load(rb)
        print('File: {}\nNumber of simulations: {}'.format(filePath, metadata[1]))
        i = 0
        while True:
            try:
                i += 1
                data = pickle.load(rb)
                print('\tGame {} winner is {}'.format(i, data[1]))
                print('\t\tPlayer 1 class is: {} deck is: {}'.format(translateClassId(data[0][0][0]), data[0][0][1]))
                print('\t\tPlayer 2 class is: {} deck is: {}'.format(translateClassId(data[0][0][2]), data[0][0][3]))
                if not isinstance(data[0][-1], str):  # bardzo brzydko
                    print('\t\tNo exception occured')
                else:
                    print('\t\tException occured:\n\t\t\t{}'.format(data[0][-1]))
            except Exception:
                break


def summarizeData(comprehensive, file=None):
    if file is not None:
        summarizeFile(file, comprehensive)
    else:
        for filepath in glob.iglob('data/*'):
            summarizeFile(filepath, comprehensive)

def mostRecentFile():
    mostRecent = None
    mostRecentFilepath = None
    for filepath in glob.iglob('data/Model-INIT/*'):
        x = filepath \
            .replace("data/", "") \
            .replace("Model-INIT\\", "") \
            .replace(".txt", "")
        if not mostRecent:
            mostRecent = datetime.strptime(x,"%d-%m-%YT%H%M%S")
            mostRecentFilepath = x
            continue
        tmp = datetime.strptime(x,"%d-%m-%YT%H%M%S")
        if mostRecent <= tmp:
            mostRecentFilepath = x
            mostRecent = tmp

    return f"data/{Configuration.INIT_MODEL_NAME}/{mostRecentFilepath}.txt"


def getGamesWithoutExceptions(filepath:str, num_games:int =50): # offset to ilosc gier do wziecia na raz
    global FILE_POSITION
    arrOfGames = []
    metadata = ()# seed i tabela wartosci, moze pozniej sie przyda
    first_iteration = True

    with open(filepath,"rb") as rb:
        while FILE_POSITION < num_games:
            try:
                if first_iteration:
                    metadata = pickle.load(rb)
                    first_iteration = not first_iteration
                elif FILE_POSITION <= num_games:
                    tmp = pickle.load(rb)
                    if not tmp:
                        FILE_POSITION -= 1
                        return
                    if tmp[1] < 4: # mniejsze od 4 to dozwolone stany gry ( nie wyjątki )
                        FILE_POSITION += 1
                        if FILE_POSITION >= num_games:
                            return metadata, arrOfGames
                        arrOfGames.append(tmp)
                    else:
                        FILE_POSITION -= 1
            except EOFError:
                return metadata, arrOfGames

        return metadata,arrOfGames



def getGamesWithoutExceptionsFromSeveralFiles(numberOfGames: int):
    cleanGames = []
    global FILE_POSITION
    FILE_POSITION = 0
    for filepath in glob.iglob('data/Model-INIT/*'):
        gamesInFile = getGamesWithoutExceptions(filepath,num_games=numberOfGames)
        if gamesInFile[0] == [] or gamesInFile[1] == []:
            continue
        cleanGames.append(gamesInFile)
    return cleanGames

def getTotalNumberOfGames():
    totalNumberOfGames = 0
    for filepath in glob.iglob('data/Model-INIT/*'):
        first_iteration = True
        with open(filepath,"rb") as rb:
            while True:
                try:
                    if first_iteration:
                        pickle.load(rb)
                        first_iteration = not first_iteration
                    else:
                        pickle.load(rb)
                        totalNumberOfGames += 1
                except EOFError:
                    break

        return totalNumberOfGames



def fileStatistics(filePath):
    games = 0
    firstWins = 0
    secondWins = 0
    draws = 0
    exceptions = 0
    with open(filePath, "rb") as rb:
        metadata = pickle.load(rb)
        while True:
            try:
                data = pickle.load(rb)
                games += 1
                if data[1] == 1:
                    firstWins += 1
                elif data[1] == 2:
                    secondWins += 1
                elif data[1] == 3:
                    draws += 1
                else:
                    exceptions += 1
            except Exception as e:
                break
    return games, firstWins, secondWins, draws, exceptions


# def loadGame(fileName, gameNumber=-1, model_name=None, pureRand = False):  # bez argumentu to ostatnia
#     if not model_name:
#         model_name = INIT_MODEL_NAME
#     model = tf.keras.models.load_model(f"Model/models/{model_name}")
#
#     with open(f"data/{model_name}/{fileName}.txt", "rb") as rb:
#         metadata = pickle.load(rb)
#         random.setstate(metadata[0])
#         np.random.seed(random.randrange(999999999))
#         tf.random.set_seed(random.randrange(999999999))
#
#         i = 0
#         gameData = None
#         while i != gameNumber:
#             i += 1
#             try:
#                 gameData = pickle.load(rb)
#             except EOFError as e:
#                 break
#         game_player = GamePlayer(model, metadata[1], metadata[2])
#         if not pureRand:
#             game_player.playGame()
#         else:
#             game_player.playRandGame()
