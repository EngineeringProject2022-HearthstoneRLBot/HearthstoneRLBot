from fireplace import cards, logging


# os.environ['PYTHONHASHSEED'] = '0' # niby mi działa z zakomentowanymi tymi liniami, ale zostawiam na później
# os.environ['CUDA_VISIBLE_DEVICES'] = '' #czy to nie zepsuje procesowania z CUDA?
from GameFiles.GameStorage import dumpGames
    #, loadGame


def main():
    cards.db.initialize()
    dumpGames()

if __name__ == "__main__":
    main()
