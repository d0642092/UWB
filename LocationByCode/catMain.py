import threading
from catTrace import catTraceT
from catEmulator import catEmulatorT

if __name__ == "__main__":
    catE = catEmulatorT()
    catT = catTraceT()
    catE.start()
    catT.start()
    catE.join()
    catT.flag = False
    catT.join()