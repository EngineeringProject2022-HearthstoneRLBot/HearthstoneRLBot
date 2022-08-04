from fireplace import cards, logging
from Tests import InputTests
from Tests.EndlessTests import continousTesting


def main():
    logger = logging.log
    logger.disabled = True
    logger.propagate = False
    cards.db.initialize()

    # networkInputTesting()
    # continousTesting()

    # myNetwork = Resnet.Network()
    # model = myNetwork.getModel()

    InputTests.test_sludge_belcher()
    InputTests.test_fiery_war_axe()
    InputTests.test_frostwolf_warlord()
    InputTests.test_blood_imp()


if __name__ == "__main__":
    main()
