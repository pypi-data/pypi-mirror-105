"""Measure you FPGA circuit!"""

__version__ = "0.1.1"

from serial import Serial
import time
from pathlib import Path

from serial.serialutil import SerialException

SERIAL = "/dev/ttyUSB1"
TIMEOUT = 100
FILENAME = "data.raw"
BYTES = 1


print("BAUDS: 12000000")

# -- Open the serial port
try:
    serial_p = Serial(SERIAL, 12000000)
    time.sleep(0.2)
except SerialException as e:
    print("Error al abrir puerto serie ")
    code, msg = e.args
    print(msg)
    exit()

print("\nWaiting for the Data from the FPGA...")
count=0;
while True:
    try:
        data = serial_p.read(BYTES)
    except KeyboardInterrupt:
        print("\nABORT...")
        break

    print(f'{hex(data[0])} ', end='', flush=True)
    count = count + 1;

    if (count % 16 == 0):
        print("")

    # Write the data into the file
    # p = Path('.')
    # f_data = p / FILENAME
    # f_data.write_bytes(data)

    # print(f"FILE: {f_data.name}\n")

serial_p.close()
