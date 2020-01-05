"""interchange message class for interchanging messages between agents and the enterprise master"""

C_MANAGERREPORTPORT=1235
C_AGENTREPORTPROC=1234

C_DEFAULTINTERVAL=10
C_DEFAULTTIMEOUTFACTOR=3 #after C_DEFAULTTIMEOUTFACTOR*C_DEFAULTINTERVAL it is assumed agent is lost

class HelloMessage:
    def __init__(self, *args, hostname="?", **kwargs):
        self.hostName = hostname
        return super().__init__(*args, **kwargs)

class InterchangeMessage:
    def __init__(self, *args, hostname = "?", dir = "", nfFiles = 0, \
        nfCreatedAvg=0, nfDeletedAvg=0, nfMovedAvg=0, nfModifiedAvg=0, \
        nfCreatedLatest=0, nfDeletedLatest=0, nfMovedLatest=0, nfModifiedLatest=0, \
        **kwargs):
        self.nfCreatedAvg = nfCreatedAvg
        self.nfDeletedAvg = nfDeletedAvg
        self.nfMovedAvg = nfMovedAvg
        self.nfModifiedAvg = nfModifiedAvg
        self.nfCreatedLatest = nfCreatedLatest
        self.nfDeletedLatest = nfDeletedLatest
        self.nfMovedLatest = nfMovedLatest
        self.nfModifiedLatest = nfModifiedLatest
        self.hostname = hostname
        self.directory = dir
        self.nfFiles = nfFiles
        return super().__init__(*args, **kwargs)
    def __str__(self):
        return """\
msg: host=%s, dir=%s, nfFiles=%s, 
nfCreatedAvg=%s, nfDeletedAvg=%s, nfMovedAvg=%s, nfModifiedAvg=%s
nfCreatedLatest=%s, nfDeletedLatest=%s, nfMovedLatest=%s, nfModifiedLatest=%s""" \
        %(self.hostname, self.directory, self.nfFiles, \
        self.nfCreatedAvg, self.nfDeletedAvg, self.nfMovedAvg, self.nfModifiedAvg, \
        self.nfCreatedLatest, self.nfDeletedLatest, self.nfMovedLatest, self.nfModifiedLatest\
        )
    def getStats(self):
        return self.nfCreatedAvg, self.nfDeletedAvg, self.nfMovedAvg, self.nfModifiedAvg, \
               self.nfCreatedLatest, self.nfDeletedLatest, self.nfMovedLatest, self.nfModifiedLatest

class _ReportMessageBase:
    def __init__(self, *args, hostname="?", directory="", message="<>", **kwargs):
        self.hostName = hostname
        self.directory = directory
        self.message = message
class AgentLostEvent(_ReportMessageBase):
    pass
class NewAgentEvent(_ReportMessageBase):
    pass
class AnomalyEvent(_ReportMessageBase):
    pass



