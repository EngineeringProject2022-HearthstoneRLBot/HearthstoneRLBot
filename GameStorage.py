import pickle
import random
import numpy as np
import tensorflow as tf
from datetime import datetime
from Model import Resnet
from GamePlayer import playGame
import glob

def translateClassId(id):
    #TODO
    return str(id)

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
                if len(data[0][-1]) != 1:
                    print('\t\tNo exception occured')
                else:
                    print('\t\tException occured:\n\t\t\t{}'.format(data[0][-1]))
            except Exception:
                break

def summarizeData(comprehensive, file = None):
    if file is not None:
        summarizeFile(file, comprehensive)
    else:
        for filepath in glob.iglob('data/*'):
            summarizeFile(filepath, comprehensive)

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


def selfPlay(model, numbgame, simulations, fileName):
    for i in range(numbgame):
        print("GAME " + str(i+1))
        state = random.getstate()
        winner, data = playGame(model, simulations)
        with open("data/" + fileName + ".txt", "ab") as fp:
            pickle.dump((data, winner, state), fp)

def dumpGames(numGames, numSims):
    fileName = datetime.now().strftime("%d-%m-%YT%H%M%S")
    with open("data/" + fileName + ".txt", "wb") as fp:  # dumpuję aktualny(pierwszy) stan randoma jako pierwszy obiekt przed zrobieniem czegokolwiek
        pickle.dump((random.getstate(), numSims), fp)
        np.random.seed(random.randrange(999999999))
        tf.random.set_seed(random.randrange(999999999))

    myNetwork = Resnet.Network()
    model = myNetwork.getModel()

    import time
    t0 = time.time()

    selfPlay(model, numGames, numSims, fileName)

    t1 = time.time()
    total = t1 - t0
    print(total)

def loadGame(fileName, gameNumber=-1): # bez argumentu to ostatnia
    with open("data/" + fileName + ".txt", "rb") as rb:
        metadata = pickle.load(rb)
        random.setstate(metadata[0])
        np.random.seed(random.randrange(999999999))
        tf.random.set_seed(random.randrange(999999999))
        myNetwork = Resnet.Network()
        model = myNetwork.getModel()

        i = 0
        gameData = None
        while i != gameNumber:
            i += 1
            try:
                gameData = pickle.load(rb)
            except Exception:
                break

        playGame(model, metadata[1], gameData[2])