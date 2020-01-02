#test the Enterprise File Monitor
import unittest
import subprocess
import shutil
import os

class Test(unittest.TestCase):
    def setUp(self):
        #generate file monitor executable for testing
        shutil.rmtree("./dist",ignore_errors=True)
        shutil.rmtree("./build", ignore_errors=True)
        shutil.rmtree("./testdir", ignore_errors=True)
        os.mkdir("./testdir")
        p = subprocess.check_call("pyinstaller -wF ./EnterpriseFileMonitorAgent.py", shell=True)
        shutil.copy("./dist/EnterpriseFileMonitorAgent.exe", "./testdir/EnterpriseFileMonitorAgent.exe")

    def testA(self):
        p = subprocess.call(".\\testdir\\EnterpriseFileMonitorAgent.exe", shell=True)
        p = subprocess.call("timeout /t 10", shell=True)
        pass

        
if __name__ == "__main__":
    unittest.main()