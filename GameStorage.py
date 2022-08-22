from GameConvinience import translateClassId
import os
import pickle
import random
import numpy as np
import tensorflow as tf
from datetime import datetime
from Model import Resnet
from GamePlayer import playGame
import glob
# ta funkcja sie przyda we wszystkim - granie najswiezszego pliku, podsumowanie najswiezszego pliku itd itd
# jak ktos sie chce podjac obstawiam ze to mega latwe będzie, taki format mamy aktualnie nazwy pliku:
# "data/"+ datetime.now().strftime("%d-%m-%YT%H%M%S") +".txt"
# więc wystarczy z tego wyciągnąć datetime.now() robiąc przeciwną operację i porównywać
from constants import INIT_MODEL_NAME, FILE_POSITION


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

    return f"data/{INIT_MODEL_NAME}/{mostRecentFilepath}.txt"

def getGamesWithoutExceptions(filepath:str, num_games:int =50): # offset to ilosc gier do wziecia na raz
    global FILE_POSITION
    arrOfGames = []
    metadata = ()# seed i tabela wartosci, moze pozniej sie przyda
    first_iteration = True

    with open(filepath,"rb") as rb:
        while True:
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

def getGamesWithoutExceptionsFromSeveralFiles(numberOfGames: int): ## nazwa jak do testow xd
    x = []
    global FILE_POSITION
    FILE_POSITION = 0
    for filepath in glob.iglob('data/Model-INIT/*'):
        d = getGamesWithoutExceptions(filepath,num_games=numberOfGames)
        if d[0] == [] or d[1] == []:
            continue
        x.append(d)


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


def selfPlay(model, numbgame, simulations, fileName, model_name):
    for i in range(numbgame):
        print("GAME " + str(i + 1))
        state = random.getstate()
        winner, data = playGame(model, simulations)
        with open(f"data/{model_name}/{fileName}.txt", "ab") as fp:
            pickle.dump((data, winner, state), fp)


def dumpGames(numGames, numSims, model_name=None):
    if not model_name:
        model_name = INIT_MODEL_NAME

    model = tf.keras.models.load_model(f"Model/models/{model_name}")
    path = f"data/{model_name}"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    fileName = datetime.now().strftime("%d-%m-%YT%H%M%S")

    with open(f"data/{model_name}/{fileName}.txt", "wb") as fp:  # dumpuję aktualny(pierwszy) stan randoma jako pierwszy obiekt przed zrobieniem czegokolwiek
        pickle.dump((random.getstate(), numSims), fp)
        np.random.seed(random.randrange(999999999))
        tf.random.set_seed(random.randrange(999999999))



    import time
    t0 = time.time()

    selfPlay(model, numGames, numSims, fileName, model_name)

    t1 = time.time()
    total = t1 - t0
    print(total)


def loadGame(fileName, gameNumber=-1, model_name=None):  # bez argumentu to ostatnia
    if not model_name:
        model_name = INIT_MODEL_NAME
    model = tf.keras.models.load_model(f"Model/models/{model_name}")

    with open(f"data/{model_name}/{fileName}.txt", "rb") as rb:
        metadata = pickle.load(rb)
        random.setstate(metadata[0])
        np.random.seed(random.randrange(999999999))
        tf.random.set_seed(random.randrange(999999999))

        i = 0
        gameData = None
        while i != gameNumber:
            i += 1
            try:
                gameData = pickle.load(rb)
            except EOFError as e:
                break

        playGame(model, metadata[1], gameData[2])


def loadParseDataForTraining():
    pass
