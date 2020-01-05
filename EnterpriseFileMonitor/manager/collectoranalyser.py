"""analyser of incoming file activity figures"""
import messages
import collections
import socket
import pickle
import select
import threading
import time

class HostDirAnalyser():
    """for each (hostname, directory) agent sending messages, a HostDirAnalyser is to be started
       and fed with regular updates originating from the agents running"""
    def __init__(self, msg, depth=1000):
        self._hostNameDir = (msg.hostname, msg.directory)
        self._nfFiles = msg.nfFiles
        self.nfCreated = collections.deque([], maxlen=depth)
        self.nfDeleted = collections.deque([], maxlen=depth)
        self.nfMoved = collections.deque([], maxlen=depth)
        self.nfModified = collections.deque([], maxlen=depth)
        self.timeoutCount=0
    def update(self, msg):
        """update with new data"""
        assert(self._hostNameDir == (msg.hostname, msg.directory)) #assure message from earlier specified host
        self.nfCreated.append(msg.nfCreatedLatest)
        self.nfDeleted.append(msg.nfDeletedLatest)
        self.nfModified.append(msg.nfModifiedLatest)
        self.nfMoved.append(msg.nfMovedLatest)
        self.timeoutCount=0
        if self._checkAnomalies():
            self.anomalyDetected()
    def anomalyDetected(self):
        pass
    def _checkAnomalies(self):
        pass

class Collector():
    """a single instance of thos class collects messages from all agents and creates one HostDirAnalyser object 
       for each agent sending update messages"""
    def __init__(self, *args, recport=messages.C_MANAGERREPORTPORT,\
                 reportport=messages.C_AGENTREPORTPROC,\
                 interval=messages.C_DEFAULTINTERVAL,\
                 timeoutfactor = messages.C_DEFAULTTIMEOUTFACTOR,\
                 **kwargs):
        self._recvSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._recvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._recvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._recvSocket.bind(("",reportport))
        self._recvSocket.setblocking(False)
        self._reportSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._reportSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._reportSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._hostDirAnalysers = {}
        self._stop=False
        self._guardThread=None
        self._runThread=None
        self._hostDirAnalysersLock = threading.Lock()
        self._interval = interval
        self._timeoutfactor = timeoutfactor 
        return super().__init__(*args, **kwargs)
    def _guard(self):
        """guard each extisting agent for continuity. If for too long no messages are received, a HostDirLost event is sent, 
           and the analyser is disposed of."""
        while self._stop==False:
            with self._hostDirAnalysersLock:
                for analyser in list(self._hostDirAnalysers):
                    self._hostDirAnalysers[analyser].timeoutCount += 1
                    if self._hostDirAnalysers[analyser].timeoutCount > self._interval*self._timeoutfactor:
                        host, thedir = analyser
                        self._reportSocket.sendto(pickle.dumps(messages.AgentLostEvent(hostname=host, directory=thedir)),
                                                  ("127.0.0.1", messages.C_MANAGERREPORTPORT))
                        self._hostDirAnalysers.pop(analyser)
            time.sleep(1)
    
    def _run(self):
        while self._stop==False:
            ready = select.select([self._recvSocket], [], [], 1)
            if ready[0]:
                msg = pickle.loads(self._recvSocket.recv(65530))
                if isinstance(msg, messages.InterchangeMessage):
                    with self._hostDirAnalysersLock:
                        if not((msg.hostname, msg.directory) in self._hostDirAnalysers):
                            #a new instance is started
                            self._reportSocket.sendto(pickle.dumps(messages.NewAgentEvent(hostname=msg.hostname, directory=msg.directory)), 
                                                      ("127.0.0.1", messages.C_MANAGERREPORTPORT))
                            self._hostDirAnalysers[(msg.hostname, msg.directory)] = HostDirAnalyser(msg)
                        else:
                            self._hostDirAnalysers[(msg.hostname, msg.directory)].update(msg)
    def run(self):
        self._guardThread = threading.Thread(target=self._guard)
        self._guardThread.start()
        self._runThread = threading.Thread(target=self._run)
        self._runThread.start()

    def stop(self):
        self._stop = True
        self._guardThread.join()
        self._runThread.join()
        self._recvSocket.close()
        self._reportSocket.close()


