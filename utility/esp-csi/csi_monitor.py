#!/usr/bin/env python3
"""
Opens a serial/socket connection to an ESP32 and listens for CSI data. 

Uses modified versions of ESP-IDF's SerialReader and StoppableThread classes.

"""
from __future__ import print_function, division
from __future__ import unicode_literals
from builtins import chr
from builtins import object
from builtins import bytes
import subprocess
import argparse
import codecs
import datetime
import re
import os
try:
    import queue
except ImportError:
    import Queue as queue
import shlex
import time
import sys
import serial
import serial.tools.miniterm as miniterm
import threading
import ctypes
import types
from distutils.version import StrictVersion
from io import open

from math import sqrt, atan2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


key_description = miniterm.key_description

# Tags for tuples in queues
TAG_KEY = 0
TAG_SERIAL = 1
TAG_SERIAL_FLUSH = 2

class StoppableThread(object):
    """
    Provide a Thread-like class which can be 'cancelled' via a subclass-provided
    cancellation method.

    Can be started and stopped multiple times.

    Isn't an instance of type Thread because Python Thread objects can only be run once
    """
    def __init__(self):
        self._thread = None

    @property
    def alive(self):
        """
        Is 'alive' whenever the internal thread object exists
        """
        return self._thread is not None

    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(target=self._run_outer)
            self._thread.start()

    def _cancel(self):
        pass  # override to provide cancellation functionality

    def run(self):
        pass  # override for the main thread behaviour

    def _run_outer(self):
        try:
            self.run()
        finally:
            self._thread = None

    def stop(self):
        if self._thread is not None:
            old_thread = self._thread
            self._thread = None
            self._cancel()
            old_thread.join()

class SerialReader(StoppableThread):
    """ Read serial data from the serial port and push to the
    event queue, until stopped.
    """
    def __init__(self, serial, event_queue):
        super(SerialReader, self).__init__()
        self.baud = serial.baudrate
        self.serial = serial
        self.queue = event_queue
        if not hasattr(self.serial, 'cancel_read'):
            # enable timeout for checking alive flag,
            # if cancel_read not available
            self.serial.timeout = 0.25

    def run(self):
        if not self.serial.is_open:
            self.serial.baudrate = self.baud
            self.serial.rts = True  # Force an RTS reset on open
            self.serial.open()
            self.serial.rts = False
        try:
            while self.alive:
                data = self.serial.read(self.serial.in_waiting or 1)
                if len(data):
                    self.queue.put((TAG_SERIAL, data), False)
        finally:
            self.serial.close()

    def _cancel(self):
        if hasattr(self.serial, 'cancel_read'):
            try:
                self.serial.cancel_read()
            except Exception:
                pass

class ESP_SerialMonitor(object):
    def __init__(self, port, baud, eol="CRLF"):
        super(ESP_SerialMonitor, self).__init__()
        self.queue = queue.Queue()
        self.serial = serial.serial_for_url(port, baud, do_not_open=True)
        socket_mode = self.serial.port.startswith("socket://")
        self.serial_reader = SerialReader(self.serial, self.queue)
        self.translate_eol = {
            "CRLF": lambda c: c.replace("\n", "\r\n"),
            "CR": lambda c: c.replace("\n", "\r"),
            "LF": lambda c: c.replace("\r", "\n"),
        }[eol]
        self.plotter = CSI_Plotter() 
        
        # internal state
        self._last_line_part = b""
        self._serial_check_exit = socket_mode


    def monitor_loop(self):
        self.serial_reader.start()
        try: 
            while self.serial_reader.alive:
                (event_tag, data) = self.queue.get()
                if event_tag == TAG_SERIAL:
                    split = data.split(b'\n') # split by line
                    if self._last_line_part != b"":
                        # add unprocessed part from previous "data" to the first line
                        split[0] = self._last_line_part + split[0]
                        self._last_line_part = b""
                    if split[-1] != b"":
                        # last part is not a full line
                        self._last_line_part = split.pop()
                    for line in split:
                        if line != b"":
                            try:
                                imaginary = []
                                real = []
                                amplitudes = []
                                phases = []
                                line = line.decode()
                                csi_string = re.findall(r"\[(.*)\]", line)[0]
                                csi_raw = [int(x) for x in csi_string.split(" ") if x != '']
                                # Create list of imaginary and real numbers from CSI
                                for i in range(len(csi_raw)):
                                    if i % 2 == 0:
                                        imaginary.append(csi_raw[i])
                                    else:
                                        real.append(csi_raw[i])

                                # Transform imaginary and real into amplitude and phase
                                for i in range(int(len(csi_raw) / 2)):
                                    amplitudes.append(sqrt(imaginary[i] ** 2 + real[i] ** 2))
                                    phases.append(atan2(imaginary[i], real[i]))
                                self.plotter.update_state(amplitudes, phases)
                                self.plotter.show()
                            except Exception:
                                pass
        finally:
            try:
                self.serial_reader.stop()
            except:
                pass

class CSI_Plotter(object):
    def __init__(self, settings=None):
        if settings:
            print("")
        self.amplitudes = []
        self.phases = []
        plt.show(block=False)
        

    def update_state(self, amplitudes, phases):
        self.amplitudes = amplitudes
        self.phases = phases
        print(self.amplitudes)

    def show(self):
        plt.cla()
        plt.title("CSI Amplitude")
        plt.xlabel("Subcarrier")
        plt.ylabel("Amplitude")
        plt.plot(self.amplitudes)
        plt.pause(.5)

def main():
    parser = argparse.ArgumentParser("csi_monitor - a serial output monitor for obtaining csi data from esp32s")

    parser.add_argument(
        '--port', '-p',
        help='Serial port device',
        default=os.environ.get('ESPTOOL_PORT', '/dev/ttyUSB0')
    )

    parser.add_argument(
        '--baud', '-b',
        help='Serial port baud rate',
        type=int,
        default=os.environ.get('MONITOR_BAUD', 921600))
    
    args = parser.parse_args()

    ESP_SerialMonitor(args.port, args.baud).monitor_loop()

if __name__ == "__main__":
    main()