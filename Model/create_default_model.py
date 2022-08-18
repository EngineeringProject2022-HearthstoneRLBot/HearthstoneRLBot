from Model import Resnet
from constants import INIT_MODEL_NAME

myNetwork = Resnet.Network()
model = myNetwork.getModel()
model.save(f'models/{INIT_MODEL_NAME}')
