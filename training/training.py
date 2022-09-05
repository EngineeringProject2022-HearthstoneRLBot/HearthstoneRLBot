import pickle

import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import backend as k
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

MODEL_NAME = "Model-INIT"
#MODEL_NAME = "test_weapon"
LEARNING_RATE = 0.00001
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

def trainNetwork(model, trainingData):
    trainingData = parseGames(trainingData)
    data = []
    for i in range(3):
        with open(f"../data/{MODEL_NAME}/05-09-2022T164550.txt", "rb") as rb:
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
        for turn in game[0][1:]: # list of turns
            if type(turn) is not str:
                if winner < 3:
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
    model.fit(x=x, y=[yPolicy, yValue], batch_size=1, epochs=5, verbose=1)

    model.save('../Model/models/TRAINED_MODEL')

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
