import os
import tensorflow as tf
import Configuration
import keras
from tensorflow.keras import backend as k

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

from GameFiles.DataGenerator import DataGenerator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def trainNetwork(model):
    trainingGenerator = DataGenerator(batch_size=1)
    # validationGenerator = DataGenerator(model_name='TRAINED_MODEL3', batch_size=1)
    # model.fit(trainingGenerator, validation_data = validationGenerator, epochs=1)
    checkpoint_dir = f"checkpoints/{Configuration.OUTPUT_MODEL_NAME}"
    callbacks = [
        # This callback saves a SavedModel every 100 batches.
        # We include the training loss in the saved model name.
        keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_dir + "/ckpt-loss={loss:.2f}", save_freq=Configuration.CALLBACK_FREQ
        )
    ]
    if Configuration.CALLBACKS == 1:
        model.fit(trainingGenerator, epochs=1, callbacks=callbacks)
    else:
        model.fit(trainingGenerator, epochs=1)
    model.save(f'../Model/models/{Configuration.OUTPUT_MODEL_NAME}')

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

model = tf.keras.models.load_model(f"../Model/models/{Configuration.INPUT_MODEL_NAME}")
model.compile(loss=['categorical_crossentropy', 'mean_squared_error'],
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
