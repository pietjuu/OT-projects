# Import pymodbus package
from pymodbus.client import ModbusTcpClient
import time

# Create connection to modbus device
RPI = ModbusTcpClient("192.168.68.117")
RPI.connect()

# Write True to coil 0 (which has an LED connected)
RPI.write_coil(0, True)
# Capture result
result = RPI.read_coils(0)
print(result)

# 10-second sleep
time.sleep(10)

# Write False to coil 0 (which has an LED connected)
RPI.write_coil(0, False)
# Capture result
result = RPI.read_coils(0)
print(result)

