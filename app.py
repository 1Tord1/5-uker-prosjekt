from flask import Flask, render_template, jsonify
import psutil
import platform  # For å sjekke OS

app = Flask(__name__)

def get_system_data():
    # CPU-bruk
    cpu = psutil.cpu_percent(interval=0.5)

    # RAM
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_used = round(ram.used / (1024**3), 2)
    ram_total = round(ram.total / (1024**3), 2)

    # CPU temperatur kun på Linux
    cpu_temp = None
    if platform.system() == "Linux":
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    cpu_temp = entry.current
                    break

    return {
        "cpu": cpu,
        "ram_percent": ram_percent,
        "ram_used": ram_used,
        "ram_total": ram_total,
        "cpu_temp": cpu_temp
    }

# Dashboard på /html
@app.route("/html")
def html_dashboard():
    data = get_system_data()
    return render_template("text.html", data=data)

# API for live oppdatering
@app.route("/api/data")
def api_data():
    data = get_system_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)