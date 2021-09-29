"""
Demo program for CSI with two ESP32s. 
Reads environment variables for ESP ports, loads example
projects at $espIDFpath.
"""

import os
import sys
import subprocess
from subprocess import PIPE
class esp:
    def __init__(self, project, port):
        self.project_path = os.getenv('project_path') + '/' + project
        self.port = port
        os.chdir(self.project_path)

    def run(self):
        os.system(
            f"sudo idf.py -p {self.port} monitor > experiment.txt"
        )

esp("active_ap", "/dev/ttyUSB0").run()
esp("active_sta", "/dev/ttyUSB1").run()