from keras.layers import Flatten, Dense, ReLU, BatchNormalization, Softmax
from tensorflow.keras import Input, Model
from Resnet import Network
import tensorflow as tf
from tensorflow.keras.applications.resnet import ResNet50

class Resnet50Ref(Network):

    def build(self):
        inputShape = (401, 41, 3)
        inputs = Input(shape=inputShape)
        model = ResNet50(include_top = False, weights = None, input_shape = (401,41,3))(inputs)
        value = Flatten()(model)
        value = Dense(128)(value)
        value = ReLU()(value)
        value = Dense(1, activation='tanh', name='win')(value)

        policy = BatchNormalization()(model)
        policy = Flatten()(policy)
        policy = Dense(252, activation='softmax', name='policy')(policy)
        model = Model(inputs, [policy, value])
        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=tf.keras.optimizers.Adam(0.01))
        return model

