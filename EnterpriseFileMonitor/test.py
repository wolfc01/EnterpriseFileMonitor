#test the Enterprise File Monitor
import unittest
import subprocess
import shutil
import os
import socket
import pickle
import time
import psutil

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
    def setUp(self):
        #generate file monitor executable for testing
        shutil.rmtree("./dist",ignore_errors=True)
        shutil.rmtree("./build", ignore_errors=True)
        shutil.rmtree("./testdir", ignore_errors=True)
        os.mkdir("./testdir")
        agentDir = os.path.join(os.path.dirname(__file__), ".\\agent")
        p = subprocess.check_call("pyinstaller -F ./EnterpriseFileMonitorAgent.py -p %s" %agentDir, shell=True)
        shutil.copy("./dist/EnterpriseFileMonitorAgent.exe", "./testdir/EnterpriseFileMonitorAgent.exe")

    def test_check_udp(self):
        testDir = os.path.join(os.path.dirname(__file__), ".\\testdir")
        p = subprocess.Popen([".\\testdir\\EnterpriseFileMonitorAgent.exe","--directory=%s" %testDir])
        g_sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        g_sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        g_sendSocket.bind(("127.0.0.1", 1234))
        msg = pickle.loads(g_sendSocket.recv(1024))
        self.assertEqual(msg.nfCreatedLatest ,0)
        g_sendSocket.close()
        kill_proc_tree(p.pid)
        p.wait()
                
if __name__ == "__main__":
    unittest.main()