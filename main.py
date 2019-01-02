#Third party packages
import multiprocessing
# Program modules
from FingerTracker import FingerTracker
from HandDisplay import Hand

if __name__ == "__main__":
    #p1 = multiprocessing.Process(target = FingerTracker)
    p2 = multiprocessing.Process(target = Hand)
    #p1.start()
    p2.start()
    #p1.join()
    p2.join()
    print("Program is closing..........................................")

