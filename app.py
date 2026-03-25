from flask import Flask, render_template, jsonify
import psutil
import platform
import time

app = Flask(__name__)

# Vi lagrer forrige disk I/O for å regne read/write per sekund
prev_disk = psutil.disk_io_counters()
prev_time = time.time()

def get_system_data():
    global prev_disk, prev_time

    # CPU
    cpu = psutil.cpu_percent(interval=0.5)

    # RAM
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_used = round(ram.used / (1024**3), 2)
    ram_total = round(ram.total / (1024**3), 2)

    # CPU temperatur (Linux / Pi only)
    cpu_temp = None
    if platform.system() == "Linux":
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    cpu_temp = entry.current
                    break

    # Diskbruk
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_used = round(disk.used / (1024**3), 2)
    disk_total = round(disk.total / (1024**3), 2)

    # Disk read/write per sekund
    current_disk = psutil.disk_io_counters()
    current_time = time.time()
    elapsed = current_time - prev_time

    read_speed = round((current_disk.read_bytes - prev_disk.read_bytes) / (1024**2) / elapsed, 2)  # MB/s
    write_speed = round((current_disk.write_bytes - prev_disk.write_bytes) / (1024**2) / elapsed, 2)  # MB/s

    # oppdater prev_disk
    prev_disk = current_disk
    prev_time = current_time

    return {
        "cpu": cpu,
        "ram_percent": ram_percent,
        "ram_used": ram_used,
        "ram_total": ram_total,
        "cpu_temp": cpu_temp,
        "disk_percent": disk_percent,
        "disk_used": disk_used,
        "disk_total": disk_total,
        "read_speed": read_speed,
        "write_speed": write_speed
    }

@app.route("/html")
def html_dashboard():
    data = get_system_data()
    return render_template("text.html", data=data)

@app.route("/api/data")
def api_data():
    data = get_system_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)