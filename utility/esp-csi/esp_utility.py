"""
Demo program for CSI with two ESP32s. 
Reads environment variables for ESP ports, loads example
projects at $espIDFpath.
"""

import os
import sys
import multiprocessing
import time
from subprocess import *
import pathlib
import signal
class esp:
    def __init__(self, project, port):
        self.project_path = os.getenv('project_path') + '/' + project
        self.port = port
        self.output = str(pathlib.Path(__file__).parent.resolve()) + f"/{project}.csv"
        os.chdir(self.project_path)
        self.base_cmd = f"idf.py -p {self.port} monitor"
        self.cmd_output = f'grep -a \"CSI_DATA\" > {self.output}'
        self.cmd = "sudo /bin/bash -c " + self.base_cmd + " | " + self.cmd_output 

    def collect(self, collection_time=15):
        process =Popen([
            "sudo",
            "/bin/bash",
            "-c",
            self.base_cmd + " | " + self.cmd_output
        ], stderr=PIPE) 
        try:
            out = process.communicate(timeout=collection_time)
            print(out)
        except TimeoutExpired:
            process.send_signal(signal.SIGINT)
            process.wait()

def collect():
    p1 = multiprocessing.Process(
        target=esp("active_ap", "/dev/ttyUSB0").collect,
        args=()
    )
    p2 = multiprocessing.Process(
        target=esp("active_sta", "/dev/ttyUSB1").collect,
        args=()
    )
    p1.start()
    p2.start()

    time.sleep(5)
    p1.kill()
    p2.kill()
    os.system('stty sane')

if __name__ == "__main__":
    collect()