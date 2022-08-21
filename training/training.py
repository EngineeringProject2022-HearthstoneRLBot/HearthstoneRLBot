import pickle

import numpy as np
import os
import tensorflow as tf
from keras import backend as k
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

MODEL_NAME = "Model-INIT"
LEARNING_RATE = 0.000001



def trainNetwork(model, trainingData):
    trainingData = parseGames(trainingData)
    data = []
    with open("../data/Model-INIT/21-08-2022T161028.txt", "rb") as rb:
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
        winner = game[1]
        for turn in game[0]:
            if type(turn) is not str:
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
    # x = [i[0] for i in trainingData]
    x = np.asarray(x)
    yPolicy = [i[1] for i in trainingData]
    yPolicy = np.asarray(yPolicy)
    yValue = [i[2] for i in trainingData]
    yValue = np.asarray(yValue)
    x = x.squeeze(1)
    model.fit(x=x, y=[yPolicy, yValue], batch_size=128, epochs=250, verbose=1)

    model.save('../Model/models/test_weapon')

def parseGames(games):
    pass

def GET_DATA():
    pass

model = tf.keras.models.load_model(f"../Model/models/{MODEL_NAME}")
model.optimizer = tf.keras.optimizers.Adam(
    learning_rate=0.001,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-07,
    amsgrad=False,
    name='Adam',
    clipnorm=1
)
k.set_value(model.optimizer.learning_rate, LEARNING_RATE)
trainNetwork(model, GET_DATA())
