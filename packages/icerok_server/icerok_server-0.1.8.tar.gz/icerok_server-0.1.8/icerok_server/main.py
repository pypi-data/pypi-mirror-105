"""Main program"""

import time
import sys
from serial import Serial
from serial.serialutil import SerialException
import icerok_server

# from pathlib import Path


SERIAL = "/dev/ttyUSB1"
TIMEOUT = 100
FILENAME = "data.raw"
BYTES = 1

print("RUNNING...")
print(f"{icerok_server.__package__}: Version {icerok_server.__version__}")
print("BAUDS: 12000000")

# -- Open the serial port
try:
    serial_p = Serial(SERIAL, 12000000)
    time.sleep(0.2)
except SerialException as exc:
    print("Error al abrir puerto serie ")
    msg = exc.args[1]
    print(msg)
    sys.exit()

print("\nWaiting for the Data from the FPGA...")
COUNT = 0
while True:
    try:
        data = serial_p.read(BYTES)
    except KeyboardInterrupt:
        print("\nABORT...\n")
        serial_p.close()
        sys.exit()

    print(f"{hex(data[0])} ", end="", flush=True)
    COUNT = COUNT + 1

    if COUNT % 16 == 0:
        print("")

    # Write the data into the file
    # p = Path('.')
    # f_data = p / FILENAME
    # f_data.write_bytes(data)

    # print(f"FILE: {f_data.name}\n")
