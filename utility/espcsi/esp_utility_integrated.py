"""
Demo program for CSI with two ESP32s. 
Reads environment variables for ESP ports, loads example
projects at $espIDFpath.
Runs csi_monitor to get CSI data back.
"""

import os
import sys
import multiprocessing
import time
from subprocess import *
import pathlib
import signal
sys.path.append(os.path.dirname(__file__))
from csi_monitor import ESP_SerialMonitor

class esp:
    def __init__(self, project, port, project_path=os.path.expanduser("~/Development/esp32-csi-tool")):
        self.project_path = project_path + '/' + project
        self.port = port
        self.output = str(pathlib.Path(__file__).parent.resolve()) + f"/{project}.csv"

    def flash(self):
        os.chdir(self.project_path)
        os.system("sudo idf.py -p {self.port} flash")

    def collect(self, end_when_motion=False):
        monitor = ESP_SerialMonitor(self.port, 115200)
        monitor.monitor_loop(end_when_motion)

def collect(fd="/dev/ttyUSB0"):
    esp("active_sta", fd).collect(False)

if __name__ == "__main__":
    collect()
