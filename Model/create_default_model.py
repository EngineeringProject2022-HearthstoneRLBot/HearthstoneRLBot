from Model import Resnet
from Model.Resnet50Ref import Resnet50Ref
from Configuration import INIT_MODEL_NAME

myNetwork = Resnet50Ref()
model = myNetwork.getModel()
model.save(f'models/{INIT_MODEL_NAME}')
