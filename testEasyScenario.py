from Model import Resnet
from GameStorage import *
import pickle
import numpy as np
import os
import tensorflow as tf
from keras import backend as k
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
m1n = 'InitTest'
m2n = 'O1Test'
m3n = 'O2Test'
m4n = 'O3Test'
numGames = 20
numSims = 4
learning_rate = 0.1

def trainNetwork(modelInName, modelOutName, repeats):
    model = loadModel(modelInName)
    k.set_value(model.optimizer.learning_rate, learning_rate)
    data = []
    for i in range(repeats):
        for filepath in glob.iglob(f'data/{modelInName}/*'):
            with open(filepath, "rb") as rb:
                metadata = pickle.load(rb)
                while True:
                    try:
                        data.append(pickle.load(rb))
                    except (EOFError, pickle.UnpicklingError):
                        break
    x = []
    yPolicy = []
    yValue = []
    moves = []
    for game in data:
        winner = game[1]  # who won the game
        for turn in game[0]:  # list of turns
            if type(turn) is not str:
                input = turn[0]
                policy = turn[1]
                yPolicy.append(policy)
                if turn[2] == winner:
                    value = 1
                elif turn[2] < 3:
                    value = 0
                else:
                    value = 0
                    continue
                x.append(input)
                yValue.append(value)
                moves.append(turn[3])
    x = np.asarray(x)
    yPolicy = np.asarray(yPolicy)
    yValue = np.asarray(yValue)
    x = x.squeeze(1)
    model.fit(x=x, y={'policy': yPolicy, 'win': yValue}, batch_size=2, epochs=5, verbose=1)
    model.save(f'Model/models/{modelOutName}')

def createDefaultModel(modelName):
    myNetwork = Resnet.Network()
    model = myNetwork.getModel()
    model.save(f'Model/models/{modelName}')

def loadModel(modelName):
    model = tf.keras.models.load_model(f'Model/models/{modelName}')
    model.optimizer = tf.keras.optimizers.Adam(
        learning_rate=0.01,
    )
    return model

def testEasyScenario():
    #createDefaultModel(m1n)
    #dumpGames(numGames, numSims, m1n)
    trainNetwork(m1n, m2n, 3)
    dumpGames(numGames, numSims, m2n)
    trainNetwork(m2n, m3n, 3)
    dumpGames(numGames, numSims, m3n)
    trainNetwork(m3n, m4n, 3)
    dumpGames(numGames, numSims, m4n)