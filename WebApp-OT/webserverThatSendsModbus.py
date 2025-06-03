# Packages
from pymodbus.client import ModbusTcpClient

# Client variables
MODBUS_SERVER_IP = "192.168.68.117"
MODBUS_PORT = 502

# function for writing values to a coil
def writecoil(address, value):
    # Configure client (IP + port)
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)
    client.connect()
    client.write_coil(address, value)
    client.close()

# function for reading value of a coil
def readcoil(address):
    # Configure client (IP + port)
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)
    client.connect()
    result =client.read_coils(address)
    client.close()
    if not result.isError():
        return result.bits[0]
    return None

