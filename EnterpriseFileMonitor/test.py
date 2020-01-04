#test the Enterprise File Monitor
import unittest
import subprocess
import shutil
import os
import socket
import pickle
import time
import psutil
import messages

def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)

class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #generate file monitor executable for testing
        shutil.rmtree("./dist",ignore_errors=True)
        shutil.rmtree("./build", ignore_errors=True)
        agentDir = os.path.join(os.path.dirname(__file__), ".\\agent")
        p = subprocess.check_call("pyinstaller -F ./EnterpriseFileMonitorAgent.py -p %s" %agentDir, shell=True)

    def setUp(self):
        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sendSocket.bind(("127.0.0.1", 1234))
        shutil.rmtree("./testdir", ignore_errors=True)
        os.mkdir("./testdir")
        shutil.copy("./dist/EnterpriseFileMonitorAgent.exe", "./testdir/EnterpriseFileMonitorAgent.exe")
        self.testDir = os.path.join(os.path.dirname(__file__), ".\\testdir")
        self.p = subprocess.Popen([".\\testdir\\EnterpriseFileMonitorAgent.exe","--directory=%s" %self.testDir, "--interval=2"])

    def tearDown(self):
        self.sendSocket.close()
        kill_proc_tree(self.p.pid)
        self.p.wait()

    def helperCheckZero(self):
        msg = pickle.loads(self.sendSocket.recv(1024))
        self.helperTests(msg, self.testDir, socket.gethostname(), 1)
        self.assertEqual(msg.nfCreatedLatest, 0)
        self.assertEqual(msg.nfDeletedLatest, 0)
        self.assertEqual(msg.nfMovedLatest, 0)
        self.assertEqual(msg.nfModifiedLatest, 0)
        self.assertEqual(msg.nfCreatedAvg, 0)
        self.assertEqual(msg.nfDeletedAvg, 0)
        self.assertEqual(msg.nfMovedAvg, 0)
        self.assertEqual(msg.nfModifiedAvg, 0)

    def helperTests(self, msg, thedir, hostname, nffiles):
        """test some things which are common"""
        self.assertTrue(isinstance(msg, messages.InterchangeMessage))
        self.assertEqual(msg.directory, thedir)
        self.assertEqual(msg.nfFiles, nffiles)
        self.assertEqual(msg.hostname, hostname)

    def test_hello(self):
        #after startup with command line parameters specifying the manager address
        #first message should be a message of type messages.HelloMessage.
        msg = pickle.loads(self.sendSocket.recv(1024))
        self.assertTrue(isinstance(msg, messages.HelloMessage))
        self.assertEqual(msg.hostName, socket.gethostname())

    def test_zero(self):
        #after startup, check if message is sent with zero changes.
        self.test_hello()
        self.helperCheckZero()

    def test_createfile(self):
        #check detection of creation of one file
        self.test_zero()
        self.helperCheckZero()
        f = open(os.path.join(self.testDir, "testfile.txt"), "w")
        f.close()
        while True:
            try:
                msg = pickle.loads(self.sendSocket.recv(1024))
                self.helperTests(msg, self.testDir, socket.gethostname(), 1)
                self.assertEqual(msg.nfCreatedLatest, 1)
                self.assertEqual(msg.nfDeletedLatest, 0)
                self.assertEqual(msg.nfMovedLatest, 0)
                self.assertEqual(msg.nfModifiedLatest, 0)
                break
            except:
                pass

    def test_modifyFiles(self):
        #test modified file detection
        self.test_createfile()
        f = open(os.path.join(self.testDir, "testfile.txt"), "a+")
        f.write("test")
        f.close()
        while True:
            try:
                msg = pickle.loads(self.sendSocket.recv(1024))
                self.helperTests(msg, self.testDir, socket.gethostname(), 1)
                self.assertEqual(msg.nfCreatedLatest, 0)
                self.assertEqual(msg.nfDeletedLatest, 0)
                self.assertEqual(msg.nfMovedLatest, 0)
                self.assertEqual(msg.nfModifiedLatest, 1)
                break
            except:
                pass
    def test_deleteFile(self):
        #test deletion detection
        self.test_createfile()
        os.remove(os.path.join(self.testDir, "testfile.txt"))
        while True:
            try:
                msg = pickle.loads(self.sendSocket.recv(1024))
                self.helperTests(msg, self.testDir, socket.gethostname(), 1)
                self.assertEqual(msg.nfCreatedLatest, 0)
                self.assertEqual(msg.nfDeletedLatest, 1)
                self.assertEqual(msg.nfMovedLatest, 0)
                self.assertEqual(msg.nfModifiedLatest, 0)
                break
            except:
                pass

    def test_moveFile(self):
        #test file move detection
        self.test_createfile()
        os.rename(os.path.join(self.testDir, "testfile.txt"), os.path.join(self.testDir, "testfilerenamed.txt"))
        while True:
            try:
                msg = pickle.loads(self.sendSocket.recv(1024))
                self.helperTests(msg, self.testDir, socket.gethostname(), 1)
                self.assertEqual(msg.nfCreatedLatest, 0)
                self.assertEqual(msg.nfDeletedLatest, 0)
                self.assertEqual(msg.nfMovedLatest, 1)
                self.assertEqual(msg.nfModifiedLatest, 0)
                break
            except:
                pass

    def test_multipleFilesCreation(self):
        """creation of multiple files: check counting"""
        NFFILES=100
        self.test_zero()
        self.helperCheckZero()
        for i in range(NFFILES):
            f = open(os.path.join(self.testDir, "testfile%s.txt" %i), "w")
            f.close()
        msg = pickle.loads(self.sendSocket.recv(1024))
        self.helperTests(msg, self.testDir, socket.gethostname(), 1)
        self.assertEqual(msg.nfCreatedLatest, NFFILES)
        self.assertEqual(msg.nfDeletedLatest, 0)
        self.assertEqual(msg.nfMovedLatest, 0)
        self.assertEqual(msg.nfModifiedLatest, 0)

        #wait for a message with zero count
        msg = pickle.loads(self.sendSocket.recv(1024))
        self.helperTests(msg, self.testDir, socket.gethostname(), 1)
        self.assertEqual(msg.nfCreatedLatest, 0)
        self.assertEqual(msg.nfDeletedLatest, 0)
        self.assertEqual(msg.nfMovedLatest, 0)
        self.assertEqual(msg.nfModifiedLatest, 0)

        #check counting of files in multiple messages sent
        for i in range(NFFILES):
            f = open(os.path.join(self.testDir, "extrafiles%s.txt" %i), "w")
            f.close()
            time.sleep(0.1)
        countedFiles = 0
        #UDP messages will be queued is the assumption here
        while True:
            msg = pickle.loads(self.sendSocket.recv(1024))
            countedFiles += msg.nfCreatedLatest
            if msg.nfCreatedLatest == 0:
                break
        self.assertEqual(countedFiles, NFFILES)

if __name__ == "__main__":
    unittest.main()