import time
import subprocess
from datetime import datetime

class SubprocessTimeoutTask:
    
    def __init__(self, timeout, timeout_step=1):
        self.stopped = False
        self.timeout = timeout
        self.step = timeout_step

    def stop(self):
        self.stopped = True

    def setSubprocess(self, p):
        self.proc = p
        current_time = datetime.now().strftime("%H:%M:%S")
        print("[TimeoutMonitor] ({}) start monitoring PID={}..".format(current_time, p.pid))

    def kill(self, pid):
        cmd = ["kill", "-9", str(pid)]
        return subprocess.call(cmd)

    def run(self):
        s = 0
        while not self.stopped and s < self.timeout:
            time.sleep(self.step)
            s += self.step
        # Check and kill process if it is timeout
        if not self.stopped and self.proc is not None:
            print("[-] Reached timeout, kill process..")
            self.kill(self.proc.pid)
            #self.proc.kill()
            #self.proc.wait()
        elif not self.stopped and self.proc is None:
            print("[-] Reached timeout, but no process handle.")
