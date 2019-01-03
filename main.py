#Third party packages
import multiprocessing
import time
#import keyboard
# Program modules
from FingerTracker import FingerTracker
from HandDisplay import Hand

if __name__ == "__main__":
    HandInput = multiprocessing.Queue()
    p1 = multiprocessing.Process(target = FingerTracker, args=(HandInput,))
    p2 = multiprocessing.Process(target = Hand, args=(HandInput,))
    p2.start()
    p1.start()
    p1.join()
    p2.join()
    HandInput.close()
    HandInput.join_thread()
    print("Program is closing..........................................")

