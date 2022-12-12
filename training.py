from GameFiles.DataGenerator import DataGenerator
import os
import Configuration
import keras
import tensorflow as tf
from tensorflow.keras import backend as k
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from math import floor
import Model.DataFunctions
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
def trainNetwork(model):
    validation_split = 0.8
    subset_factor = 1 # put 1 to train and validate all data, I have used 0.003 to have only 40 samples in train and 10 in validation
    epoch_num = 50
    trainingGenerator = DataGenerator(batch_size=Configuration.BATCH_SIZE)
    validationGenerator = DataGenerator(batch_size=Configuration.BATCH_SIZE)

    # it is already shuffled, so we can do it this way
    validationGenerator.list_IDs = trainingGenerator.list_IDs[
                                    floor(validation_split*subset_factor*len(trainingGenerator)):
                                    floor(subset_factor*len(trainingGenerator.list_IDs))]
    trainingGenerator.list_IDs = trainingGenerator.list_IDs[
                                    0:
                                    floor(validation_split*subset_factor*len(trainingGenerator.list_IDs))]

    # update of indexes + shuffle again
    trainingGenerator.on_epoch_end()
    validationGenerator.on_epoch_end()

    # trainingGenerator.set_wv_func(Model.DataFunctions.diminishingValue)
    # validationGenerator = DataGenerator(model_name='TRAINED_MODEL3', batch_size=1)
    # model.fit(trainingGenerator, validation_data = validationGenerator, epochs=1)
    checkpoint_dir = f"Model/checkpoints/{Configuration.OUTPUT_MODEL_NAME}"
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_dir + "/ckpt-loss={loss:.2f}", save_freq=Configuration.CALLBACK_FREQ
        )
    ]
    if Configuration.CALLBACKS == 1:
        model.fit(trainingGenerator,
                  steps_per_epoch=len(trainingGenerator),
                  epochs=epoch_num,
                  validation_data=validationGenerator,
                  validation_steps=len(validationGenerator),
                  callbacks=callbacks)
    else:
        model.fit(trainingGenerator,
                  steps_per_epoch=len(trainingGenerator),
                  epochs=epoch_num,
                  validation_data=validationGenerator,
                  validation_steps=len(validationGenerator))
    model.save(f'Model/models/{Configuration.OUTPUT_MODEL_NAME}')

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

model = tf.keras.models.load_model(f"Model/models/{Configuration.INPUT_MODEL_NAME}")
print(model.summary())
model.compile(loss=['kl_divergence', 'mean_squared_error'],
              loss_weights = [Configuration.POLICY_WEIGHT, Configuration.WINVALUE_WEIGHT], optimizer=tf.keras.optimizers.Adam(Configuration.LEARNING_RATE))
# model.optimizer = tf.keras.optimizers.Adam(
#     learning_rate=0.001,
#     beta_1=0.9,
#     beta_2=0.999,
#     epsilon=1e-07,
#     amsgrad=False,
#     name='Adam',
#     clipnorm=1
# )
k.set_value(model.optimizer.learning_rate, Configuration.LEARNING_RATE)
trainNetwork(model)
