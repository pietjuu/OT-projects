import time
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException

# Configuration
MODBUS_SERVER_IP = "192.168.68.117"
MODBUS_PORT = 502
POLL_INTERVAL = 1

def main():
    # Configure client (IP + port)
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)

    if not client.connect():
        print("Failed to connect to Modbus server.")
        return

    try:
        while True:
            result = client.read_coils(0)

            if isinstance(result, ModbusIOException):
                print("Modbus IO exception occurred.")
            elif result.isError():
                print("Modbus error reading coil.")
            else:
                coil_value = result.bits[0]
                print(f"Coil 0 value: {coil_value}")

            time.sleep(POLL_INTERVAL)

    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
