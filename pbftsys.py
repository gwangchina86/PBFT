#!/usr/bin/env python3

import random
import threading
from pbftthread import PBFTThread

class PBFTSys:

    def __init__(self, iprimary, request, ntotal, ibad, maxlag, reply):
        self.iprimary = iprimary
        self.request = request
        self.ntotal = ntotal
        self.ibad = ibad
        self.maxlag = maxlag
        self.reply = reply
        self.threads = []
        self.messages = {}

    def info(self):
        print("==================================================")
        print("PBFTSys:")
        print("==================================================")
        print("Total number of thread: %d." % self.ntotal)
        print("ID of the primary: %d." % self.iprimary)
        print("Indices of bad thread: ", self.ibad)
        print("Max lag: %f." % self.maxlag)

    def run(self):
        self.info()
        self.initMessage()
        #print(self.messages)
        #tlock = threading.Lock()
        for i in range(self.ntotal):
            self.threads.append(PBFTThread(i, self.messages))
        for t in self.threads:
            t.start()

        # send request to the primary
        # the primary multicasts the request to the backups
        # replicas execute the request and send a reply to the client
        # wait for (f + 1) replies from replicas with the same result

        f = (self.ntotal - 1) // 3
        while len(self.messages[-1]) < 2 * f + 1:
            pass
        for r in self.messages[-1]:
            self.reply[r] += 1

        for t in self.threads:
            t.join()
        print(self.messages[-1])

    def initMessage(self):
        for i in range(self.ntotal):
            self.messages[i] = {}
            self.messages[i]["tid"] = i
            self.messages[i]["ntotal"] = self.ntotal
            self.messages[i]["primary"] = True if i == self.iprimary else False
            self.messages[i]["bad"] = True if i in self.ibad else False
            self.messages[i]["lag"] = random.uniform(0, self.maxlag)
            self.messages[i]["request"] = self.request if i == self.iprimary else None
            self.messages[i]["prepare"] = []
            self.messages[i]["commit"] = []
        self.messages[-1] = []   # reply

