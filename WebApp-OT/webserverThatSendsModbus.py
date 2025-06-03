# Packages
from pymodbus.client import ModbusTcpClient
import time
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Client variables
MODBUS_SERVER_IP = "192.168.68.117"
MODBUS_PORT = 502

# function for writing values to a coil
def writecoil(address, value):
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)
    client.connect()
    client.write_coil(address, value)
    client.close()

# function for reading value of a coil
def readcoil(address, value):
    client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)
    client.connect()
    client.read_coils(address)
    client.close()

