from Model import Resnet
from Model.Resnet import Network
from Model.Resnet50Ref import Resnet50Ref
INIT_MODEL_NAME = "Model-INIT"

myNetwork = Network()
model = myNetwork.getModel()
model.save(f'models/{INIT_MODEL_NAME}')
