from fireplace import cards, logging


# os.environ['PYTHONHASHSEED'] = '0' # niby mi działa z zakomentowanymi tymi liniami, ale zostawiam na później
# os.environ['CUDA_VISIBLE_DEVICES'] = '' #czy to nie zepsuje procesowania z CUDA?
import testEasyScenario
from GameStorage import dumpGames, loadGame
from constants import GAME_NUM, SIMULATION_NUM


def main():
    logger = logging.log
    logger.disabled = True
    logger.propagate = False
    cards.db.initialize()


# i Models/models
    # mozemy podac argument model_name
    # wystarczy same imie nie trzeba sciezki
    # default(nie trzeba wpisywac) = Model-INIT
    # tak samo dla loadgame
    dumpGames(GAME_NUM, SIMULATION_NUM, pureRand=True)
    #dumpGames(GAME_NUM, SIMULATION_NUM)
    #testEasyScenario.testEasyScenario()
    #loadGame("30-08-2022T183257", 2,model_name="test_weapon5")
    #summarizeData(False)

    #... patrz niżej co tu wg mnie fajnie byłoby zrobić
    #runTests()
    #trainModel("XYZ.txt")
    #playRealGame()


# da rade zrobić plik Tests.py w tests i tam umieścić wszystkie testy na raz?(oprócz tych wymagających typu EndlessTests)
# mam taką myśl, że każdy z naszych 'procesów' będzie miał jedną metodę 'start', np. narazie odpalamy skrypt w jednym
# z kilku celów: dumpowanie gier do trenowania, załadowanie jakiejś gry(jak przestaniemy mieć błędy to to przejdzie do czegoś bliżej testów), robienie testów,
# później dojdzie trenowanie i granie(pewnie o czymś jeszcze zapomniałem), więc taki mam pomysł aby po prostu każda z tych akcji miała
# coś w stylu metody 'start'
# czyli np Tests.runTests() odpalałoby te 5 linii na dole i wszystkie inne testy które nie są czasochłonne



if __name__ == "__main__":
    main()
