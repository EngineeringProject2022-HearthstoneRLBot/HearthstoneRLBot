from fireplace import cards, logging

# import os
# os.environ['PYTHONHASHSEED'] = '0' # niby mi działa z zakomentowanymi tymi liniami, ale zostawiam na później
# os.environ['CUDA_VISIBLE_DEVICES'] = '' #czy to nie zepsuje procesowania z CUDA?
from GameStorage import dumpGames, loadGame, summarizeData

GAME_NUM = 1000
SIMULATION_NUM = 20

def main():
    logger = logging.log
    logger.disabled = True
    logger.propagate = False
    cards.db.initialize()

#zróbcie sobie folder 'data'
    dumpGames(GAME_NUM, SIMULATION_NUM)
    #loadGame("11-08-2022T002609")
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
    #InputTests.test_sludge_belcher()
    #InputTests.test_fiery_war_axe()
    #InputTests.test_frostwolf_warlord()
    #InputTests.test_blood_imp()


if __name__ == "__main__":
    main()
