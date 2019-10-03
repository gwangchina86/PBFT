#!usr/bin/env python3

import threading
import time

class PBFTThread (threading.Thread):

    def __init__(self, threadID, messages, printinfo = False):
        threading.Thread.__init__(self)
        self.tid = threadID
        self.primary = True if messages[self.tid]["primary"] else False
        self.bad = True if messages[self.tid]["bad"]  else False
        self.lag = messages[self.tid]["lag"]
        self.messages = messages
        self.badprimary = False
        #self.tlock = tlock
        self.printinfo = printinfo

    def info(self):
        if self.primary:
            print("Primary {} ({}): lag = {}".format(self.tid, "B" if self.bad else "G", self.lag))
        else:
            print("Backup {} ({}): lag = {}".format(self.tid, "B" if self.bad else "G", self.lag))

    def run(self):
        if self.printinfo:
            self.info()
        # send request to the primary
        # the primary multicasts the request to the backups
        # replicas execute the request and send a reply to the client
        # wait for (f + 1) replies from replicas with the same result
        self.pre_prepare()
        self.prepare()
        self.commit()
        self.reply()

    def pre_prepare(self):
        if self.primary:
            request = self.messages[self.tid]["request"]
            # if the thread is primary, send request to backups
            if self.bad:
                self.badprimary = True
                if self.messages[self.tid]["attack"] == "invalid":
                    request = "block"
                else:
                    time.sleep(5 * self.messages[self.tid]["maxlag"])
            for tid in self.messages.keys():
                if tid != -1 and tid != self.tid:
                    self.messages[tid]["request"] = request
            if self.printinfo:
                print("Thread %d is pre-prepared." % self.tid)
        return

    def prepare(self):
        if not self.primary:
            # the backups receive request from the primary
            while self.messages[self.tid]["request"] == None:
                pass
            time.sleep(self.lag)
            self.checkrequest()
            self.messages[self.tid]["prepare"].append(self.tid)
            #print("Thread %d received request." % self.tid)
            # the backups send prepare messagess to other threads
            time.sleep(self.lag)
            for tid in self.messages.keys():
                if tid != -1:
                    self.messages[tid]["prepare"].append(self.tid)
                    #print(self.tid, " send message to ", tid)
            if self.printinfo:
                print("Thread %d is prepared." % self.tid)
        return

    def commit(self):
        # when 2f + 1 threads are ready, commit
        n = len(self.messages.keys())
        f = (n - 1) // 3
        while len(self.messages[self.tid]["prepare"]) < 2 * f + 1:
            pass
        self.messages[self.tid]["commit"].append(self.tid)
        if self.printinfo:
            print("Thread %d is ready to commit." % self.tid)
        time.sleep(self.lag)
        for tid in self.messages.keys():
            if tid != -1 and tid != self.tid:
                self.messages[tid]["commit"].append(self.tid)
        if self.printinfo:
            print("Thread %d committed." % self.tid)

    def reply(self):
        if (self.bad ^ self.badprimary) and self.messages[self.tid]["attack"] in ["invalid", None]:
            time.sleep(self.lag)
            self.messages[-1].append(0)
        else:
            time.sleep(self.lag)
            self.messages[-1].append(1)

    def checkrequest(self):
        if self.messages[self.tid]["request"] != "BLOCK":
            self.badprimary = True

