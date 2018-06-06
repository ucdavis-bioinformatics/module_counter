#!/usr/bin/env python
 
import socket
import time
import copy
import sys
from threading import Thread
from SocketServer import ThreadingMixIn
from Queue import Queue
from collections import defaultdict
import glob
import os.path

# echo -e "bwa\t1.2.3" | nc -w 0 localhost 12345

class CountThread(Thread):
    def __init__(self,count):
        Thread.__init__(self)
        self.count = count
        #print "Count thread started...\n"

    def run(self):
        while True:
            time.sleep(86400)
            #print "Writing counts file...\n"
            count_copy = copy.deepcopy(self.count)
            timestr = time.strftime("%Y%m%d_%H%M%S")
            count_file = open("counts."+timestr+".out","w")
            for mod in count_copy:
                for ver,cnt in count_copy[mod].iteritems():
                    count_file.write(mod+"\t"+ver+"\t"+str(cnt)+"\n")
            count_file.close()

class QueueThread(Thread):
    def __init__(self,q,count):
        Thread.__init__(self)
        self.q = q
        self.count = count

    def run(self):
        while True:
            modstr = q.get()
            #print modstr
            (mod,ver,userstr) = modstr.split('\t')
            if ver in count[mod]:
                count[mod][ver] += 1
            else:
        cfs = [n for n in glob("counts.[0-9]*_[0-9]*.out") if os.path.isfile(n)]        count[mod][ver] = 1

 
class ClientThread(Thread):
 
    def __init__(self,ip,port,q):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.q = q
        #print "[+] New thread started for "+ip+":"+str(port)
 
 
    def run(self):
        while True:
            data = conn.recv(2048)
            if not data: break
            #print "received data:", data
            data = data.rstrip()
            q.put(data)
            #conn.send(data)  # echo
 
TCP_IP = '0.0.0.0'
TCP_PORT = 12345
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
 
 
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

count = defaultdict(dict)

if len(sys.argv) == 2:
    f = open(sys.argv[1],"r")
    for line in f:
        line = line.rstrip('\n')
        data = line.split('\t')
        count[data[0]][data[1]] = data[2]

else:
    cfs = [n for n in glob.glob("counts.[0-9]*_[0-9]*.out") if os.path.isfile(n)]
    if cfs:
        cfs.sort()
        f = open(cfs[-1],"r")
        for line in f:
            line = line.rstrip('\n')
            data = line.split('\t')
            count[data[0]][data[1]] = data[2]

q = Queue()
qthread = QueueThread(q,count)
qthread.start()
countthread = CountThread(count)
countthread.start()
 
while True:
    tcpsock.listen(4)
    #print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    newthread = ClientThread(ip,port,q)
    newthread.start()
    threads.append(newthread)
 
qthread.join()
countthread.join()
for t in threads:
    t.join()
