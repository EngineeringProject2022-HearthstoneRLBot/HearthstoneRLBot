from fireplace import cards
from GameInterface.AIPlayer import AIPlayer
from GameInterface.ManualPlayer import ManualPlayer
from GameInterface.ModeledGame import ModeledGame
from GameInterface.RandomPlayer import RandomPlayer


def main():
    print('x')
    cards.db.initialize()
    deck1 = ['EX1_169', 'EX1_169', 'EX1_154', 'EX1_154', 'CS2_011', 'CS2_011', 'CS2_013', 'CS2_013', 'EX1_166',
             'EX1_166', 'CS2_012', 'CS2_012', 'EX1_165', 'EX1_165', 'EX1_571', 'NEW1_008', 'NEW1_008', 'EX1_573',
             'FP1_001', 'EX1_085', 'FP1_005', 'FP1_005', 'EX1_005', 'GVG_096', 'GVG_096', 'EX1_284', 'EX1_558',
             'FP1_012', 'EX1_016', 'GVG_110']
    deck2 = ['GVG_043', 'GVG_043', 'BRM_013', 'BRM_013', 'NEW1_031', 'NEW1_031', 'EX1_536', 'EX1_536', 'EX1_539',
             'EX1_539', 'EX1_538', 'EX1_538', 'CS2_188', 'CS2_188', 'EX1_008', 'EX1_008', 'EX1_029', 'EX1_029',
             'FP1_002', 'FP1_002', 'NEW1_019', 'NEW1_019', 'AT_084', 'AT_084', 'EX1_089', 'EX1_089', 'AT_087', 'AT_087',
             'CS2_203', 'CS2_203']
    p1 = AIPlayer("X", 3, deck1, "Model-INIT", 2)
    #p2 = AIPlayer("Y", 4, deck2, "Model-INIT", 2)
    #p1 = RandomPlayer("X", 3, deck1)
    #p2 = RandomPlayer("Y", 4, deck2, False)
    p2 = ManualPlayer("Ja", 5, deck2)
    game = ModeledGame(p1, p2)
    game.start()

if __name__ == "__main__":
    main()
