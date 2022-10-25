from fireplace import cards, logging
from GameFiles.GameStorage import dumpGames
from Configuration import NUM_THREADS, OUTPUT_FOLDER
from MultiThreading.ModelFW import ModelFW
import threading

cards.db.initialize()
ModelFW.threads = NUM_THREADS
threads = []
for i in range(NUM_THREADS):
    thread = threading.Thread(target = dumpGames, args = [OUTPUT_FOLDER+str(i)])
    thread.start()
    threads.append(thread)

for t in threads:
    t.join()