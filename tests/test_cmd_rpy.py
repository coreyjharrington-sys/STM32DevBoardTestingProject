  
def send_and_receive(ser, cmd):
    ser.write((cmd + "\r\n").encode("utf-8"))
    return ser.readline().decode("utf-8").strip()

def test_status(ser):
    reply = send_and_receive(ser, "STATUS")
    assert reply == "OK"

def test_version(ser):
    reply = send_and_receive(ser, "VERSION")
    assert reply == "v1.0"

def test_add(ser):
    reply = send_and_receive(ser, "ADD 5 7")
    assert reply == "12"

def test_subtract(ser):
    reply = send_and_receive(ser, "SUBTRACT 10 3")
    assert reply == "7"

def test_multiply(ser):
    reply = send_and_receive(ser, "MULTIPLY 4 6")
    assert reply == "24"

def test_divide_valid(ser):
    reply = send_and_receive(ser, "DIVIDE 10 3")
    assert reply == "3 (remainder 1)"

def test_divide_by_zero(ser):
    reply = send_and_receive(ser, "DIVIDE 7 0")
    assert reply == "Error: divide by zero"

def test_invalid_command(ser):
    reply = send_and_receive(ser, "FOO")
    assert reply == "Unknown command"
