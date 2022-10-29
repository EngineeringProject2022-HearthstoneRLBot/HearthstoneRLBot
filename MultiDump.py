
import os
os.environ['TF_XLA_FLAGS']='--tf_xla_auto_jit=2'
from fireplace import cards, logging
from GameFiles.GameStorage import dumpGames
from Configuration import NUM_THREADS, OUTPUT_FOLDER
from MultiThreading.ModelFW import ModelFW
import threading


def main():
    cards.db.initialize()
    ModelFW.threads = NUM_THREADS
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target = dumpGames, args = [OUTPUT_FOLDER+str(i)])
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()