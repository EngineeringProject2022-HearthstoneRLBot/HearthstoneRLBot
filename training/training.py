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


def weighted_categorical_crossentropy(weights):
    """
    A weighted version of keras.objectives.categorical_crossentropy

    Variables:
        weights: numpy array of shape (C,) where C is the number of classes

    Usage:
        weights = np.array([0.5,2,10]) # Class one at 0.5, class 2 twice the normal weights, class 3 10x.
        loss = weighted_categorical_crossentropy(weights)
        model.compile(loss=loss,optimizer='adam')
    """

    weights_heavy = weights[:]
    weights_heavy[-1] = 10
    _weights = K.variable(weights)
    _weights_heavy = K.variable(weights_heavy)

    def loss(y_true, y_pred):
        # scale predictions so that the class probas of each sample sum to 1
        y_pred /= K.sum(y_pred, axis=-1, keepdims=True)
        # clip to prevent NaN's and Inf's
        y_pred = K.clip(y_pred, K.epsilon(), 1 - K.epsilon())
        # calc
        check = K.greater(y_pred[0, -1], y_true[0, -1])
        weights_final = K.switch(
            check,
            _weights_heavy,
            _weights
        )
        loss = y_true * K.log(y_pred) * weights_final
        loss = -K.sum(loss, -1)
        return loss

    return loss


loss = weighted_categorical_crossentropy([np.ones(252)])
model = tf.keras.models.load_model(f"../Model/models/{Configuration.INPUT_MODEL_NAME}", custom_objects={"loss": loss})

boundaries = [10000, 80000]
values = [0.00001, 0.00001, 0.000001]
lr = tf.keras.optimizers.schedules.PiecewiseConstantDecay(boundaries, values)
# lr = Configuration.LEARNING_RATE

model.compile(loss=[loss, 'mean_squared_error'],
              loss_weights=[Configuration.POLICY_WEIGHT, Configuration.WINVALUE_WEIGHT],
              optimizer=tf.keras.optimizers.Adam(lr))
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
