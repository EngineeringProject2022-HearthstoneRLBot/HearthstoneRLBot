import tensorflow as tf
import threading
import numpy as np

class ModelFW:
    threads = 1
    models = {}
    lock = threading.Lock()
    @staticmethod
    def getModel(modelName):
        ModelFW.lock.acquire(True)
        if modelName not in ModelFW.models:
            if ModelFW.threads > 1:
                ModelFW.models[modelName] = MultiThreadedModel(modelName)
            else:
                ModelFW.models[modelName] = SingleThreadModel(modelName)
        ModelFW.lock.release()
        return ModelFW.models[modelName]

class SingleThreadModel:
    def __init__(self, name):
        self.model = tf.keras.models.load_model(f"./Model/models/{name}")
        self.factor = 1 if len(name) < 4 or name[:4] != 'Norm' else 30
    def __call__(self, x):
        return self.model(x*self.factor)

class MultiThreadedModel:
    def __init__(self, name):
        #self.model = tf.keras.models.load_model(f"./Model/models/{name}")
        self.model = SingleThreadModel(name)
        self.insertLock = threading.Lock()
        self.outputLock = threading.Condition()
        self.inputs = None
        self.policies = None
        self.wins = None
        self.i = 1

    def getOutput(self, i):
        return self.policies[None, i], self.wins[None, i]

    def __call__(self, x):
        self.insertLock.acquire(True)
        level = None
        if self.inputs is None:
            level = 0
            self.inputs = x
        else:
            level = np.shape(self.inputs)[0]
            self.inputs = np.append(self.inputs, x, axis = 0)
        self.insertLock.release()
        if level == ModelFW.threads-1:
            self.i += 1
            self.outputLock.acquire()
            policies, wins = self.model(self.inputs)
            self.policies = policies.numpy()
            self.wins = wins.numpy()
            self.inputs = None
            self.outputLock.notify_all()
            self.outputLock.release()
            return self.getOutput(level)
        else:
            with self.outputLock:
                self.outputLock.wait()
                return self.getOutput(level)
