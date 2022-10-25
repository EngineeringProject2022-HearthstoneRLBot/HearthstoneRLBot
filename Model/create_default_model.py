from Model import Resnet
from Model.Resnet import Network
from Model.Resnet50Ref import Resnet50Ref
from Model.TestModel import TestModel

INIT_MODEL_NAME = "Model-TEST"

myNetwork = Network()
model = myNetwork.getModel()
model.save(f'models/{INIT_MODEL_NAME}')
