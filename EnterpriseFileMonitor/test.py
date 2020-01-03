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
        testDir = os.path.join(os.path.dirname(__file__), ".\\testdir")
        self.p = subprocess.Popen([".\\testdir\\EnterpriseFileMonitorAgent.exe","--directory=%s" %testDir])

    def tearDown(self):
        self.sendSocket.close()
        kill_proc_tree(self.p.pid)
        self.p.wait()
        
    def test_check_hello(self):
        #after startup with command line parameters specifying the manager address
        #first message should be a message of type messages.HelloMessage.
        msg = pickle.loads(self.sendSocket.recv(1024))
        self.assertTrue(isinstance(msg, messages.HelloMessage))
        self.assertEqual(msg.hostName, socket.gethostname())

if __name__ == "__main__":
    unittest.main()