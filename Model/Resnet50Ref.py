from keras.layers import Flatten, Dense, ReLU, BatchNormalization, Softmax, ZeroPadding2D
from tensorflow.keras import Input, Model
from Resnet import Network
import tensorflow as tf
from tensorflow.keras.applications.resnet import ResNet50

class Resnet50Ref(Network):

    def build(self):
        inputShape = (401, 41, 3)
        inputs = Input(shape=inputShape)
        inputs = ZeroPadding2D(padding=(2, 2))(inputs)
        x = ResNet50(include_top=False, weights=None)
        print(x.summary())
        model = ResNet50(include_top = False, weights = None)(inputs)
        model = Flatten()(model)
        model = Dense(512, activation = 'relu')(model)
        value = Dense(256, activation = 'relu')(model)
        value = Dense(1, activation='tanh', name='win')(value)
        policy = Dense(252, activation='softmax', name='policy')(model)
        model = Model(inputs, [policy, value])
        print(model.summary())
        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=tf.keras.optimizers.Adam(0.01))
        return model

