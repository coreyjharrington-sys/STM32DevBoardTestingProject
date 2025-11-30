# test_cdc_parser.py
import json
import pytest
import serial
import time
import logging
from serial.tools import list_ports

def getDUTconfig():
    with open("dut_config.json") as json_file:
        return json.load(json_file)["STM32DevBoard"]

def getPortByVIDPID(VID, PID):
    for port in list_ports.comports():
        if(port.vid == VID, port.pid == PID):
            logging.info(port.device)
            return port.device
#    raise ValueError("No COM port for Device")

@pytest.fixture(scope="module")
def ser():
    # Adjust COM port and baud rate for your setup
#    port = "COM9"       # Windows example; use "/dev/ttyACM0" on Linux
    baud = 115200       # ignored for USB CDC, required for UART

    dut_cfg = getDUTconfig()

    baud = dut_cfg["baudrate"]
    DUT_VID = int(dut_cfg["vid"], 16)
    DUT_PID = int(dut_cfg["pid"], 16)

    #Finds com port from device PID and VID
    port = getPortByVIDPID(DUT_VID, DUT_PID)
    if not port:
        pytest.skip("No Arduino device found")
    logging.info("Serial Connection fixture start")

    #port = getPortByVIDPID(0x0483, 0x5740)  # VID/PID for STM32 CDC device
    s = serial.Serial(port, baud, timeout=1)
    time.sleep(2)       # give port time to settle
    yield s
    s.close()
