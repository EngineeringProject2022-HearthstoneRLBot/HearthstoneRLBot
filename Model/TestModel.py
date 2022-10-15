from keras import Input, Model
from keras.layers import Dense

from Model.Resnet import Network
import tensorflow as tf

class TestModel(Network):

    def build(self):
        inputShape = (401, 41, 3)
        inputs = Input(shape=inputShape)
        model = self.buildConvLayer(inputs)
        value_head = self.buildValueHead(model)
        policy_head = self.buildPolicyHead(model)
        model = Model(inputs, [policy_head, value_head])
        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=tf.keras.optimizers.Adam(0.01))
        return model
