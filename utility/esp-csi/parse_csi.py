import re
from math import sqrt, atan2
import sys
import matplotlib.pyplot as plt


if __name__ == "__main__":
    """
    This script file demonstrates how to transform raw CSI out from the ESP32 into CSI-amplitude and CSI-phase.
    Updated by Zachary Kauffman.
    """
    if len(sys.argv) < 2:
        exit(1)

    FILE_NAME = sys.argv[1] 
    f = open(FILE_NAME)
    plt.title("CSI Amplitude by Subcarrier")
    plt.ylabel('Amplitude')
    plt.xlabel('Subcarrier')
    for j, l in enumerate(f.readlines()):
        imaginary = []
        real = []
        amplitudes = []
        phases = []

        # Parse string to create integer list
        csi_string = re.findall(r"\[(.*)\]", l)[0]
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
    plt.plot(amplitudes)
    plt.show()