import datetime
from math import floor

from fireplace import cards
from keras.callbacks import Callback
from GameFiles.DataGenerator import DataGenerator
import os
import tensorflow as tf
import Configuration
import keras
from tensorflow.keras import backend as k
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorboard.plugins.hparams import api as hp
import Model.DataFunctions
from GameInterface import PlayerType
from GameInterface.GameCreator import GameCreator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

run_dir = 'logs/hparam_tuning/' + datetime.datetime.now().strftime("%d-%m-%YT%H%M%S")
with tf.summary.create_file_writer('logs/hparam_tuning').as_default():
    hp.hparams_config(
        hparams=Configuration.HPARAMS,
        metrics=[hp.Metric(Configuration.METRIC_ACCURACY)]
    )


# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class TestCallbacks(Callback):
    def __init__(self):
        self.batch_number = -1
        Configuration.LOG_TREE = True

    def on_batch_end(self, batch, logs=None):
        # checkpoint_dir = f"Model/checkpoints/{Configuration.OUTPUT_MODEL_NAME}"
        if self.batch_number % Configuration.CALLBACK_FREQ == 0 and self.batch_number != 0:
            if not cards.db.initialized:
                cards.db.initialize()
            sep = lambda: print('\n', "#" * 50, '\n')
            GameCreator.createFireballTest(
                modelp1=f"../checkpoints/{Configuration.OUTPUT_MODEL_NAME}/ckpt-loss={logs['loss']:.2f}",
                simulationsp1=50).start()
            sep()
            GameCreator.createDruidTestGame(
                modelp1=f"../checkpoints/{Configuration.OUTPUT_MODEL_NAME}/ckpt-loss={logs['loss']:.2f}",
                simulationsp1=50).start()
            sep()
            GameCreator.createHunterTestGame(
                modelp1=f"../checkpoints/{Configuration.OUTPUT_MODEL_NAME}/ckpt-loss={logs['loss']:.2f}",
                simulationsp1=50).start()
            sep()
            GameCreator.createLeperGnomeTest(
                modelp1=f"../checkpoints/{Configuration.OUTPUT_MODEL_NAME}/ckpt-loss={logs['loss']:.2f}",
                simulationsp1=50).start()
            sep()
            GameCreator.createMageTestGame(
                modelp1=f"../checkpoints/{Configuration.OUTPUT_MODEL_NAME}/ckpt-loss={logs['loss']:.2f}",
                simulationsp1=50).start()
            sep()
            GameCreator.createSmartTradeTest(
                modelp1=f"../checkpoints/{Configuration.OUTPUT_MODEL_NAME}/ckpt-loss={logs['loss']:.2f}",
                simulationsp1=50).start()
            sep()
            GameCreator.createWeaponTest(
                modelp1=f"../checkpoints/{Configuration.OUTPUT_MODEL_NAME}/ckpt-loss={logs['loss']:.2f}",
                simulationsp1=50).start()
        self.batch_number += 1


def trainNetwork(model):
    validation_split = 0.75
    subset_factor = 1  # put 1 to train and validate all data, I have used 0.003 to have only 40 samples in train and 10 in validation
    epoch_num = 50
    trainingGenerator = DataGenerator(batch_size=Configuration.hparams[Configuration.BATCH_SIZE])
    validationGenerator = DataGenerator(batch_size=Configuration.hparams[Configuration.BATCH_SIZE])
    # it is already shuffled, so we can do it this way
    validationGenerator.list_IDs = trainingGenerator.list_IDs[
                                   floor(validation_split * subset_factor * len(trainingGenerator)):
                                   floor(subset_factor * len(trainingGenerator.list_IDs))]
    trainingGenerator.list_IDs = trainingGenerator.list_IDs[
                                 0:
                                 floor(validation_split * subset_factor * len(trainingGenerator.list_IDs))]

    # update of indexes + shuffle again
    trainingGenerator.on_epoch_end()
    validationGenerator.on_epoch_end()

    # trainingGenerator.set_wv_func(Model.DataFunctions.diminishingValue)
    # validationGenerator = DataGenerator(model_name='TRAINED_MODEL3', batch_size=1)
    # model.fit(trainingGenerator, validation_data = validationGenerator, epochs=1)
    checkpoint_dir = f"Model/checkpoints/{Configuration.OUTPUT_MODEL_NAME}"
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir="./logs/" + datetime.datetime.now().strftime("%d-%m-%YT%H%M%S"),
        histogram_freq=0,
        write_graph=False,
        write_images=False,
        write_steps_per_second=False,
        profile_batch=0,
        embeddings_freq=0,
        embeddings_metadata=None
    )
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_dir + "/ckpt-loss={loss:.2f}", save_freq=Configuration.CALLBACK_FREQ
        ),
        # TestCallbacks(),
        tensorboard_callback,
        hp.KerasCallback("logs/hparam_tuning", Configuration.hparams),  # log hparams
    ]
    if Configuration.CALLBACKS == 1:
        a = model.fit(trainingGenerator,
                      steps_per_epoch=len(trainingGenerator),
                      epochs=epoch_num,
                      validation_data=validationGenerator,
                      validation_steps=len(validationGenerator),
                      callbacks=callbacks)
    else:
        a = model.fit(trainingGenerator,
                      steps_per_epoch=len(trainingGenerator),
                      epochs=epoch_num,
                      validation_data=validationGenerator,
                      validation_steps=len(validationGenerator)
                      )

    model.save(f'Model/models/{Configuration.OUTPUT_MODEL_NAME}')
    return a.history["val_loss"][-1]


config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

model = tf.keras.models.load_model(f"Model/models/{Configuration.INPUT_MODEL_NAME}")
print(model.summary())
if Configuration.hparams[Configuration.OPTIMIZER] == "adam":
    optimizer = tf.keras.optimizers.Adam(Configuration.hparams[Configuration.LEARNING_RATE])
else:
    optimizer = tf.keras.optimizers.SGD(Configuration.hparams[Configuration.LEARNING_RATE])
model.compile(loss=['kl_divergence', 'mean_squared_error'],
              metrics=['accuracy'],
              loss_weights=[Configuration.hparams[Configuration.POLICY_WEIGHT],
                            Configuration.hparams[Configuration.WINVALUE_WEIGHT]],
              optimizer=optimizer)
# model.optimizer = tf.keras.optimizers.Adam(
#     learning_rate=0.001,
#     beta_1=0.9,
#     beta_2=0.999,
#     epsilon=1e-07,
#     amsgrad=False,
#     name='Adam',
#     clipnorm=1
# )

# k.set_value(model.optimizer.learning_rate, Configuration.LEARNING_RATE)
with tf.summary.create_file_writer(run_dir).as_default():
    hp.hparams(Configuration.hparams)
    accuracy = trainNetwork(model)
    tf.summary.scalar(Configuration.METRIC_ACCURACY, accuracy, step=1)

# def trainNetwork(model):
#     validation_split = 0.8
#     subset_factor = 1 # put 1 to train and validate all data, I have used 0.003 to have only 40 samples in train and 10 in validation
#     epoch_num = 50
#     trainingGenerator = DataGenerator(batch_size=Configuration.BATCH_SIZE)
#     validationGenerator = DataGenerator(batch_size=Configuration.BATCH_SIZE)
#
#     # it is already shuffled, so we can do it this way
#     validationGenerator.list_IDs = trainingGenerator.list_IDs[
#                                     floor(validation_split*subset_factor*len(trainingGenerator)):
#                                     floor(subset_factor*len(trainingGenerator.list_IDs))]
#     trainingGenerator.list_IDs = trainingGenerator.list_IDs[
#                                     0:
#                                     floor(validation_split*subset_factor*len(trainingGenerator.list_IDs))]
#
#     # update of indexes + shuffle again
#     trainingGenerator.on_epoch_end()
#     validationGenerator.on_epoch_end()
#
#     # trainingGenerator.set_wv_func(Model.DataFunctions.diminishingValue)
#     # validationGenerator = DataGenerator(model_name='TRAINED_MODEL3', batch_size=1)
#     # model.fit(trainingGenerator, validation_data = validationGenerator, epochs=1)
#     checkpoint_dir = f"Model/checkpoints/{Configuration.OUTPUT_MODEL_NAME}"
#     callbacks = [
#         keras.callbacks.ModelCheckpoint(
#             filepath=checkpoint_dir + "/ckpt-loss={loss:.2f}", save_freq=Configuration.CALLBACK_FREQ
#         )
#     ]
#     if Configuration.CALLBACKS == 1:
#         model.fit(trainingGenerator,
#                   steps_per_epoch=len(trainingGenerator),
#                   epochs=epoch_num,
#                   validation_data=validationGenerator,
#                   validation_steps=len(validationGenerator),
#                   callbacks=callbacks)
#     else:
#         model.fit(trainingGenerator,
#                   steps_per_epoch=len(trainingGenerator),
#                   epochs=epoch_num,
#                   validation_data=validationGenerator,
#                   validation_steps=len(validationGenerator))
#     model.save(f'Model/models/{Configuration.OUTPUT_MODEL_NAME}')
