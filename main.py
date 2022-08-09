import pickle

from fireplace import cards, logging

from GamePlayer import selfplay
from Model import Resnet
from Tests import InputTests
from Tests.EndlessTests import continousTesting


def main():
    logger = logging.log
    logger.disabled = True
    logger.propagate = False
    cards.db.initialize()

    # networkInputTesting()
    # continousTesting()

    # data = None
    # with open("TrainingData.txt", "rb") as rb:
    #     while True:
    #         data = pickle.load(rb)

    myNetwork = Resnet.Network()
    model = myNetwork.getModel()



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
