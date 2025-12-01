# test_cdc_parser.py
import json
import pytest
import serial
import time
import logging
from serial.tools import list_ports
#from urllib3 import request

#helper function to send command and receive reply
def send_and_receive(ser, cmd):
    ser.write((cmd + "\r\n").encode("utf-8"))
    return ser.readline().decode("utf-8").strip()

#pulls device configuration from JSON file
def getDUTconfig():
    with open("dut_config.json") as json_file:
        return json.load(json_file)["STM32DevBoard"] #returns dictionary

#helper function to get port by VID and PID
def getPortByVIDPID(VID, PID):
    for port in list_ports.comports():
        if(port.vid == VID, port.pid == PID):
            logging.info(port.device)
            return port.device
#    raise ValueError("No COM port for Device")

#adds the option for mocking serial connection
def pytest_addoption(parser):
    parser.addoption(
        "--mock",
        action="store_true",
        default=False,
        help="Run tests in mock mode"
    )

#class for mocking serial connection
class MockSerial:
    def __init__(self):
        self.buffer = b"" #empty instance varible to store mock write data

    def write(self, data):
        self.buffer = data

    def readline(self):

        if self.buffer == b'STATUS\r\n':
            return b'OK\r\n'
        elif self.buffer == b'VERSION\r\n':
            return b'v1.0\r\n'
        elif self.buffer == b'ADD 5 7\r\n':
            return b'12\r\n'
        elif self.buffer == b'SUBTRACT 10 3\r\n':
            return b'7\r\n'
        elif self.buffer == b'MULTIPLY 4 6\r\n':
            return b'24\r\n'
        elif self.buffer == b'DIVIDE 10 3\r\n':
            return b'3 (remainder 1)\r\n'
        elif self.buffer == b'DIVIDE 7 0\r\n':
            return b'Error: divide by zero\r\n'
        else:
            return b'Unknown command\r\n'
    def close(self):
        pass

#fixture for serial connection (mock or real)
@pytest.fixture(scope="module")
def ser(request):

    use_mock = request.config.getoption("--mock")

    if use_mock:
        # Setup mock serial connection or return a mock object
        s = MockSerial()
    else:
        #Creates dictionary object from JSON file
        dut_cfg = getDUTconfig() 

        #Reads baudrate, VID, and PID from dictionary
        baud = dut_cfg["baudrate"]
        DUT_VID = int(dut_cfg["vid"], 16)
        DUT_PID = int(dut_cfg["pid"], 16)

        #Finds com port from device PID and VID
        port = getPortByVIDPID(DUT_VID, DUT_PID)
        if not port:
            pytest.skip("No STM32DevBoard device found")
        #Setup real serial connection
        s = serial.Serial(port, baud, timeout=1)
        time.sleep(2)       # give port time to settle

    yield s #returns serial connection object
    s.close()  # Teardown serial connection after test
