import pickle
from datetime import datetime

from fireplace import cards, logging
import numpy as np
import random
import tensorflow as tf
from GamePlayer import selfplay ,playGame
from Model import Resnet
from Tests import InputTests
from Tests.EndlessTests import continousTesting

# import os
# os.environ['PYTHONHASHSEED'] = '0' # niby mi działa z zakomentowanymi tymi liniami, ale zostawiam na później
# os.environ['CUDA_VISIBLE_DEVICES'] = '' #czy to nie zepsuje procesowania z CUDA?

GAME_NUM = 3
SIMULATION_NUM = 2

def dumpTrainingGames(numGames, numSims):
    fileName = datetime.now().strftime("%d-%m-%YT%H%M%S")
    with open("data/" + fileName + ".txt", "wb") as fp:  # dumpuję aktualny(pierwszy) stan randoma jako pierwszy obiekt przed zrobieniem czegokolwiek
        pickle.dump((random.getstate(), SIMULATION_NUM), fp)
        np.random.seed(random.randrange(999999999))
        tf.random.set_seed(random.randrange(999999999))

    myNetwork = Resnet.Network()
    model = myNetwork.getModel()

    import time
    t0 = time.time()

    selfplay(model, numGames, numSims, fileName)

    t1 = time.time()
    total = t1 - t0
    print(total)

def loadGame(fileName, gameNumber=-1): # bez argumentu to ostatnia
    with open("data/" + fileName + ".txt", "rb") as rb:
        metadata = pickle.load(rb)
        random.setstate(metadata[0])
        np.random.seed(random.randrange(999999999))
        tf.random.set_seed(random.randrange(999999999))
        myNetwork = Resnet.Network()
        model = myNetwork.getModel()

        i = 0
        gameData = None
        while i != gameNumber:
            i += 1
            try:
                gameData = pickle.load(rb)
            except Exception:
                break

        playGame(model, metadata[1], gameData[2])

def main():
    logger = logging.log
    logger.disabled = True
    logger.propagate = False
    cards.db.initialize()
    # networkInputTesting()
    # continousTesting()

    dumpTrainingGames(GAME_NUM, SIMULATION_NUM)
#    loadGame("10-08-2022T234739")


    #InputTests.test_sludge_belcher()
    #InputTests.test_fiery_war_axe()
    #InputTests.test_frostwolf_warlord()
    #InputTests.test_blood_imp()


if __name__ == "__main__":
    main()
