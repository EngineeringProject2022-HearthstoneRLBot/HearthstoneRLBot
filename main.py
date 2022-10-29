import os

from fireplace import cards, logging
import tensorflow as tf

# os.environ['PYTHONHASHSEED'] = '0' # niby mi działa z zakomentowanymi tymi liniami, ale zostawiam na później
#os.environ['CUDA_VISIBLE_DEVICES'] = '-1' #czy to nie zepsuje procesowania z CUDA?
from GameFiles.GameStorage import dumpGames
    #, loadGame

def main():
    tf.config.experimental.enable_tensor_float_32_execution(False)
    cards.db.initialize()
    dumpGames()

if __name__ == "__main__":
    main()

