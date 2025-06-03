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
    result =client.read_coils(address)
    client.close()
    if not result.isError():
        return result.bits[0]
    return None

# When user visit home page (/) run readcoil function and store it in coil_0, then store that in the html
@app.route("/")
def index():
    coil_0 = readcoil(0)
    return render_template("index.html", coil_0=coil_0)

# When user clicks the coil/on run write coil function and pass True to it
@app.route("/coil/on")
def coil_on():
    writecoil(0, True)
    return redirect(url_for("index"))

# When user clicks the coil/ff run write coil function and pass False to it
@app.route("/coil/off")
def coil_off():
    writecoil(0, False)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="O.0.0.0", port=5000, debug=True)