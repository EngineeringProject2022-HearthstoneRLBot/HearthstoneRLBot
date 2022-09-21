from tensorflow.keras import Input, Model
from Resnet import Network
import tensorflow as tf
from tensorflow.keras.applications.resnet import ResNet50

class Resnet50Ref(Network):

    def build(self):
        inputShape = (401, 41, 3)
        inputs = Input(shape=inputShape)
        base_model = ResNet50(include_top = False, input_shape = (401,41,3))
        x = base_model(inputs)
        value_head = self.buildValueHead(x)
        policy_head = self.buildPolicyHead(x)
        model = Model(inputs, [policy_head, value_head])
        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=tf.keras.optimizers.Adam(0.01))
        return model

