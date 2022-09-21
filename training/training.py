import os
import tensorflow as tf
from tensorflow.keras import backend as k

from DataGenerator import DataGenerator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

MODEL_NAME = "TRAINED_MODEL3"
#MODEL_NAME = "test_weapon5"
LEARNING_RATE = 0.001
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

def trainNetwork(model, trainingData):
    trainingGenerator = DataGenerator(model_name='Model-INIT',batch_size=4)
    validationGenerator = DataGenerator(model_name='TRAINED_MODEL3', batch_size=1)
    model.fit(trainingGenerator, validation_data = validationGenerator, epochs=1)
    model.save('../Model/models/TRAINED_MODEL4')

def parseGames(games):
    pass

def GET_DATA():
    pass

model = tf.keras.models.load_model(f"../Model/models/{MODEL_NAME}")
model.compile(loss=['categorical_crossentropy', 'mean_squared_error'],
              loss_weights = [0, 1], optimizer=tf.keras.optimizers.SGD(0.001))
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
