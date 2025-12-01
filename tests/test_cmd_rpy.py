import pytest
from conftest import send_and_receive

@pytest.mark.smoke
def test_status(ser):
    reply = send_and_receive(ser, "STATUS")
    assert reply == "OK"

@pytest.mark.smoke
def test_version(ser):
    reply = send_and_receive(ser, "VERSION")
    assert reply == "v1.0"

@pytest.mark.regression
def test_add(ser):
    reply = send_and_receive(ser, "ADD 5 7")
    assert reply == "12"

@pytest.mark.regression
def test_subtract(ser):
    reply = send_and_receive(ser, "SUBTRACT 10 3")
    assert reply == "7"

@pytest.mark.regression
def test_multiply(ser):
    reply = send_and_receive(ser, "MULTIPLY 4 6")
    assert reply == "24"

@pytest.mark.regression
def test_divide_valid(ser):
    reply = send_and_receive(ser, "DIVIDE 10 3")
    assert reply == "3 (remainder 1)"

@pytest.mark.regression
def test_divide_by_zero(ser):
    reply = send_and_receive(ser, "DIVIDE 7 0")
    assert reply == "Error: divide by zero"

@pytest.mark.regression
def test_invalid_command(ser):
    reply = send_and_receive(ser, "FOO")
    assert reply == "Unknown command"
