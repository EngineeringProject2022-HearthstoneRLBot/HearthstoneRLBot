from fireplace import cards
from GameInterface.AIPlayer import AIPlayer
from GameInterface.DiscardingGame import DiscardingGame
from GameInterface.ManualPlayer import ManualPlayer
from GameInterface.ModeledGame import ModeledGame
from GameInterface.RandomPlayer import RandomPlayer


def main():
    print('x')
    cards.db.initialize()
    deck1 = ['CS2_072', 'CS2_072', 'CS2_074', 'CS2_074', 'CS2_189', 'CS2_189', 'CS1_042', 'CS1_042', 'CS2_075',
                  'CS2_075', 'CS2_172', 'CS2_172', 'EX1_050', 'EX1_050', 'EX1_581', 'EX1_581', 'CS2_141', 'CS2_141',
                  'EX1_025', 'EX1_025', 'CS2_147', 'CS2_147', 'CS2_131', 'CS2_131', 'CS2_076', 'CS2_076', 'EX1_593',
                  'EX1_593', 'CS2_150', 'CS2_150']
    deck2 = ['EX1_169', 'EX1_169', 'CS2_005', 'CS2_005', 'CS2_189', 'CS2_189', 'CS2_120', 'CS2_120', 'CS2_009',
                  'CS2_009', 'CS2_013', 'CS2_013', 'CS2_007', 'CS2_007', 'CS2_127', 'CS2_127', 'CS2_182', 'CS2_182',
                  'CS2_119', 'CS2_119', 'DS1_055', 'DS1_055', 'EX1_593', 'EX1_593', 'CS2_200', 'CS2_200', 'CS2_162',
                  'CS2_162', 'CS2_201', 'CS2_201']
    #p1 = AIPlayer("Model", 3, deck1, "TRAINED_MODEL6", 20, True)
    #p2 = AIPlayer("Y", 4, deck2, "Model-INIT", 2)
    #p1 = RandomPlayer("X", 3, deck1)
    #p1 = RandomPlayer("Rogue", 7, deck1, False)
    p1 = AIPlayer("RogueModel", 7, deck1, "TRAINED_MODEL6", 10, True)
    p2 = RandomPlayer("Druid", 2, deck2, False)
    #p2 = AIPlayer("Ja", 3, deck2, "TRAINED_MODEL6", 20)
    #game = ModeledGame(p1, p2)
    n = 0
    i = 0
    while True:
        game = ModeledGame(p1, p2)
        game.start()
        if game.winner == 1:
            if game.game.player1.name == game.player1.name:
                i+=1
        elif game.winner == 2:
            if game.game.player2.name == game.player1.name:
                i+=1
        n+=1
        print(f'{p1.name} won {i}/{n} times. WR: {i/n}')

if __name__ == "__main__":
    main()
