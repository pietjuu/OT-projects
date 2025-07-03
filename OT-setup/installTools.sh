#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "[*] Updating and upgrading system packages..."
sudo apt update && sudo apt upgrade -y

echo "[*] Installing Metasploit Framework..."
sudo apt install metasploit-framework -y

echo "[*] Creating Python virtual environment for MITM tools..."
sudo python3 -m venv ~/mitm_env

echo "[*] Activating virtual environment..."
# shellcheck disable=SC1090
source ~/mitm_env/bin/activate

echo "[*] Updating package list again inside the virtual environment..."
sudo apt update

echo "[*] Installing NetfilterQueue in virtual environment..."
pip install NetfilterQueue

echo "[*] Upgrading system packages again..."
sudo apt upgrade -y

echo "[*] Installing Scapy..."
sudo apt install scapy -y

echo "[*] Running final upgrade and Scapy install as root..."
sudo apt upgrade -y
sudo apt install scapy -y

echo "[*] Inserting iptables rules to forward MODBUS TCP traffic to NFQUEUE..."
sudo iptables -I FORWARD -p tcp --dport 502 -j NFQUEUE --queue-num 1 --queue-bypass
sudo iptables -I FORWARD -p tcp --sport 502 -j NFQUEUE --queue-num 1 --queue-bypass

echo "[*] Current iptables FORWARD chain rules:"
sudo iptables -L FORWARD -v -n --line-numbers | grep 'tcp.*502'

echo "[*] All setup steps completed."
