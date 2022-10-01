from Model import Resnet
from Model.Resnet50Ref import Resnet50Ref
INIT_MODEL_NAME = "Model-INIT"

myNetwork = Resnet50Ref()
model = myNetwork.getModel()
model.save(f'models/{INIT_MODEL_NAME}')
