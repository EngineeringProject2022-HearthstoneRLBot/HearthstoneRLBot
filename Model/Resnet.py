from tensorflow.keras.models import Model
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Input
import tensorflow as tf
from tensorflow.python.keras.layers import ReLU, Add

class Network:
    def __init__(self):
        self.theModel = self.build()

    def getModel(self):
        return self.theModel

    def build(self):
        inputShape = (401, 41, 3)
        inputs = Input(shape=inputShape)
        network = self.buildConvLayer(inputs)
        for i in range(15):
            network = self.buildResLayer(network)
        network = self.buildResLayer(network)
        value_head = self.buildValueHead(network)
        policy_head = self.buildPolicyHead(network)
        model = Model(inputs, [policy_head, value_head])
        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=tf.keras.optimizers.Adam(0.01))
        return model

    def buildValueHead(self, inputs):
        value = Conv2D(filters=1, kernel_size=1, strides=1)(inputs)
        value = self.bn_relu(value)
        value = Flatten()(value)
        value = Dense(256)(value)
        value = ReLU()(value)
        #initializer = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.05, seed=None)
        value = Dense(1, activation='tanh', name = 'win')(value)
        return value

    def buildPolicyHead(self, inputs):
        policy = Conv2D(filters=2, kernel_size=1, strides=1)(inputs)
        policy = self.bn_relu(policy)
        policy = Flatten()(policy)
        #initializer = tf.keras.initializers.RandomNormal(mean=0.05, stddev=0.001, seed=None)
        policy = Dense(252, activation='softmax', name = 'policy')(policy)
        return policy

    def buildConvLayer(self, inputs):
        conv = Conv2D(padding='same', filters=256, strides=1, kernel_size=3)(inputs)
        conv = self.bn_relu(conv)
        return conv

    def buildResLayer(self, inputs):
        block = self.buildConvLayer(inputs)
        block = Conv2D(padding='same', filters=256, strides=1, kernel_size=3)(block)
        block = BatchNormalization()(block)
        skip = Add()([inputs, block])
        skip = ReLU()(skip)
        return skip

    def bn_relu(self, inputs):
        relu = BatchNormalization()(inputs)
        bn = ReLU()(relu)
        return bn

