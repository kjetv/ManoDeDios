#Third party packages
import multiprocessing
import time
# Program modules
from FingerTracker import FingerTracker
from HandDisplay import Hand


def fingerPos(q):
	start = time.time()
	while True:
		end = time.time()
		millis = float(end-start)
		q.put(millis*100)
		time.sleep(0.01)
		#print(millis)
		if millis >= 10:
			break

if __name__ == "__main__":
    HandInput = multiprocessing.Queue()
    p1 = multiprocessing.Process(target = FingerTracker, args=(HandInput,))
    p2 = multiprocessing.Process(target = Hand, args=(HandInput,))
    p2.start()
    #fingerPos(HandInput)
    p1.start()
    p1.join()
    HandInput.close()
    HandInput.join_thread()
    p2.join()
    print("Program is closing..........................................")

