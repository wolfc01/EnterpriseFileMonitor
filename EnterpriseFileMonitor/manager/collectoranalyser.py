"""analyser of incoming file activity figures"""
import messages
import collections
import threading
import socket

class HostDirAnalyser():
    def __int__(self, msg, depth=1000):
        self._hostNameDir = (msg.hostname, msg.directory)
        self._nfFiles = msg.nfFiles
        self.nfCreated = collections.deque([], maxlen=depth)
        self.nfDeleted = collections.deque([], maxlen=depth)
        self.nfMoved = collections.deque([], maxlen=depth)
        self.nfModified = collections.deque([], maxlen=depth)
    def update(self, msg):
        """update with new data"""
        assert(self._hostNameDir == (msg.hostname, msg.directory)) #assure message from earlier specified host
        self.nfCreated.append(self.nfCreatedLatest)
        self.nfDeleted.append(msg.nfDeletedLatest)
        self.nfModified.append(msg.nfModifiedLatest)
        self.nfMoved.append(msg.nfMovedLatest)
        if self._checkAnomalies():
            self.anomalyDetected()
    def anomalyDetected(self):
        pass
    def _checkAnomalies(self):
        pass

class Collector():
    def __init__(self, *args, port=messages.C_REPORTPORT, **kwargs):
        self._recvSocket = socket.socket(('', port))
        self._recvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._recvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._reportSocket = socket.socket(('127.0.0.1', port))
        self._reportSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._reportSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        return super().__init__(*args, **kwargs)
    def run(self):



