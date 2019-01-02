#Third party packages
import multiprocessing
# Program modules
from FingerTracker import FingerTracker

if __name__ == "__main__":
    p1 = multiprocessing.Process(target = FingerTracker)
    p1.start()
    p1.join()
    print("Program is closing..........................................")

