from flask import Flask, render_template, redirect, url_for
import webserverThatSendsModbus

app = Flask(__name__)

# When user visit home page (/) run readcoil function and store it in coil_0, then store that in the html
@app.route("/")
def index():
    coil_0 = webserverThatSendsModbus.readcoil(0)
    return render_template("index.html", coil_0=coil_0)

# When user clicks the coil/on run write coil function and pass True to it
@app.route("/coil/on")
def coil_on():
    webserverThatSendsModbus.writecoil(0, True)
    return redirect(url_for("index"))

# When user clicks the coil/ff run write coil function and pass False to it
@app.route("/coil/off")
def coil_off():
    webserverThatSendsModbus.writecoil(0, False)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)