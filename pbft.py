#!/usr/bin/env python3

import random
import time
from pbftsys import PBFTSys

def main():
    print("Starting a PBFT simulation...")
    nsim = 100
    ntotal = 13
    maxlag = 0.1
    ibad = [1, 3, 10, 12]
    #ibad = [1, 3, 10, 12, 0, 5]
    #ibad = [1, 3, 10, 12, 0, 5, 6, 9]
    attack = "invalid"
    #attack = "slowdown1"   # not finished yet  TODO
    #attack = "slowdown2"   # not finished yet  TODO
    vstart = 1
    print("ntotal = %d, nbad = %d, maxlag = %f, nsim = %d." % (ntotal, len(ibad), maxlag, nsim))
    printinfo = False
    tt = 0
    nsucc = 0
    for i in range(nsim):
        [deltat, status] = placeablock(ntotal, ibad, maxlag, vstart, attack, printinfo)
        tt += deltat
        if status:
            nsucc += 1
        print("Sim %d, deltat = %f, status = %d." % (i, deltat, status))
    print("Total time = %f." % tt)
    print("Average time = %f." % (tt/nsim))
    print("%d blocks are successfully places in %d simulations." % (nsucc, nsim))
    print("End of the simulation.")
    return

def placeablock(ntotal, ibad, maxlag, vstart, attack = "invalid", printinfo = False):
    request = "BLOCK"
    f = (ntotal - 1) // 3
    iview = vstart
    reply = {0 : 0, 1 : 0}
    tt = 0
    while reply[1] < f + 1:
        reply = {0 : 0, 1 : 0}
        iprimary = iview % ntotal
        if printinfo:
            print("view = %d, primary = %d." % (iview, iprimary))
        tbegin = time.time()
        pbftsys = PBFTSys(iprimary, request, ntotal, ibad, maxlag, reply, attack, printinfo)
        pbftsys.run()
        tend = time.time()
        tt += tend - tbegin
        if printinfo:
            print("Reply: ", reply)
            print("This round takes ", tend - tbegin, " seconds.")
            if reply[1] < f + 1:
                print("Bad view, change primary.")
        iview += 1
    if iprimary in ibad:
        if printinfo:
            print("block is placed.")
        status = False
    else:
        if printinfo:
            print("BLOCK is placed.")
        status = True
    return [tt, status]

if __name__ == "__main__":
    main()
