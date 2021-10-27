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
from csi_monitor import ESP_SerialMonitor

class esp:
    def __init__(self, project, port, project_path=os.path.expanduser("/home/zkauff/Development/esp32-csi-tool")):
        self.project_path = project_path + '/' + project
        self.port = port
        self.output = str(pathlib.Path(__file__).parent.resolve()) + f"/{project}.csv"

    def flash(self):
        os.chdir(self.project_path)
        os.system("sudo idf.py -p {self.port} flash")

    def collect(self):
        monitor = ESP_SerialMonitor(self.port, 115200)
        monitor.monitor_loop()

def collect():
    #esp("active_ap", "/dev/ttyUSB1")
    esp("active_sta", "/dev/ttyUSB0").collect()

if __name__ == "__main__":
    collect()
