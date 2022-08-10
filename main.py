import pickle

from fireplace import cards, logging
import numpy as np
import random
import tensorflow as tf
from GamePlayer import selfplay ,playGame
from Model import Resnet
from Tests import InputTests
from Tests.EndlessTests import continousTesting

import os
os.environ['PYTHONHASHSEED'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '' #czy to nie zepsuje procesowania z CUDA?


def main():
    logger = logging.log
    logger.disabled = True
    logger.propagate = False
    cards.db.initialize()

    # networkInputTesting()
    # continousTesting()

    # fileName = "09-08-2022T200803"
    # with open("data/"+fileName+".txt", "rb") as rb:
    #    while True:
    #        data = pickle.load(rb)
    #        random.setstate(data[0][0])
    #        np.random.seed(random.randrange(999999999))
    #        tf.random.set_seed(random.randrange(999999999))
    myNetwork = Resnet.Network()
    model = myNetwork.getModel()
    #        playGame(model, 4, fileName, data[0][0])

    import time
    t0 = time.time()
    selfplay(1, model, 4)
    t1 = time.time()

    total = t1 - t0
    print(total)
    InputTests.test_sludge_belcher()
    InputTests.test_fiery_war_axe()
    InputTests.test_frostwolf_warlord()
    InputTests.test_blood_imp()


if __name__ == "__main__":
    main()
