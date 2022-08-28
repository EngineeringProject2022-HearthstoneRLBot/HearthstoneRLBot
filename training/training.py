import pickle

import numpy as np
import os
import tensorflow as tf
from keras import backend as k
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

MODEL_NAME = "Model-INIT"
LEARNING_RATE = 0.000001

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

def trainNetwork(model, trainingData):
    trainingData = parseGames(trainingData)
    data = []
    for i in range(13):
        with open(f"../data/{MODEL_NAME}/25-08-2022T213323.txt", "rb") as rb:
            metadata = pickle.load(rb)
            while True:
                try:
                    data.append(pickle.load(rb))
                except (EOFError, pickle.UnpicklingError):
                    break
    x = []
    yPolicy = []
    yValue = []
    for game in data:
        winner = game[1] # who won the game
        for turn in game[0]: # list of turns
            if type(turn) is not str:
                if turn[2] == 2 and winner < 3:
                    input = turn[0]
                    x.append(input)
                    policy = turn[1]
                    yPolicy.append(policy)
                    if turn[2] == winner:
                        value = 1
                    elif turn[2] < 3:
                        value = -1
                    else:
                        value = 0
                    yValue.append(value)
    x = np.asarray(x)
    yPolicy = np.asarray(yPolicy)
    yValue = np.asarray(yValue)
    x = x.squeeze(1)
    model.fit(x=x, y=[yPolicy, yValue], batch_size=1, epochs=20, verbose=1)

    model.save('../Model/models/test_weapon5')

def parseGames(games):
    pass

def GET_DATA():
    pass

model = tf.keras.models.load_model(f"../Model/models/{MODEL_NAME}")
# model.optimizer = tf.keras.optimizers.Adam(
#     learning_rate=0.001,
#     beta_1=0.9,
#     beta_2=0.999,
#     epsilon=1e-07,
#     amsgrad=False,
#     name='Adam',
#     clipnorm=1
# )
k.set_value(model.optimizer.learning_rate, LEARNING_RATE)
trainNetwork(model, GET_DATA())
