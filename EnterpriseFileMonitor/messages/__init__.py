"""interchange message class for interchanging messages between agents and the enterprise master"""

class interchangeMessage:
    def __init__(self, *args, hostname = "?", dir = "", nfFiles = 0, nfCreated=0.0, nfDeleted=0.0, nfMoved=0.0, nfModified=0.0, **kwargs):
        self.nfCreated = nfCreated
        self.nfDeleted = nfDeleted
        self.nfMoved = nfMoved
        self.nfModified = nfModified
        self.hostname = hostname
        self.directory = dir
        self.nfFiles = nfFiles
        return super().__init__(*args, **kwargs)
    def __str__(self):
        return "msg: host=%s, dir=%s, nfFiles=%s, nfCreated=%s, nfDeleted=%s, nfMoved=%s, nfModified=%s" \
            %(self.hostname, self.directory, self.nfFiles, self.nfCreated, self.nfDeleted, self.nfMoved, self.nfModified)
    def getStats(self):
        return self.nfCreated, self.nfDeleted, self.nfMoved, self.nfModified

