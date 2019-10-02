#!/usr/bin/env python3

import random
import time
from pbftsys import PBFTSys

def main():
    print("Starting a PBFT simulation...")
    ntotal = 13
    nbad = 4
    maxlag = 1.0
    request = "BLOCK"
    #ibad = random.sample(range(ntotal), nbad)  # indices of bad nodes
    ibad = [1, 3, 10, 12]
    reply = {0 : 0, 1 : 0}
    f = (ntotal - 1) // 3
    iview, iprimary = 0, 0
    while reply[1] < f + 1:
        reply = {0 : 0, 1 : 0}
        iview += 1
        iprimary = iview % ntotal
        print("view = %d, primary = %d." % (iview, iprimary))
        tbegin = time.time()
        pbftsys = PBFTSys(iprimary, request, ntotal, ibad, maxlag, reply)
        pbftsys.run()
        tend = time.time()
        print("Reply: ", reply)
        print("This round takes ", tend - tbegin, " second.")
        if reply[1] < f + 1:
            print("Bad view, change primary.")
    print("BLOCK is placed.")
    return

if __name__ == "__main__":
    main()
