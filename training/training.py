import pickle

import numpy as np
import os
import tensorflow as tf
from tensorflow.keras import backend as k

from HearthstoneRLBot.DataGenerator import DataGenerator

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
    trainingGenerator = DataGenerator(model_name='Model-INIT',batch_size=4)
    model.fit_generator(generator=trainingGenerator,workers=1,use_multiprocessing=False,epochs=5)
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
