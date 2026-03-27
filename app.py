from flask import Flask, render_template, jsonify
import psutil
import platform
import time

# import for RAM-hastighet
if platform.system() == "Windows":
    try:
        import wmi
    except ImportError:
        wmi = None

app = Flask(__name__)

prev_disk = psutil.disk_io_counters()
prev_time = time.time()

def get_ram_speed():
    if platform.system() == "Windows" and wmi:
        try:
            c = wmi.WMI()
            for mem in c.Win32_PhysicalMemory():
                return int(mem.MaxClockSpeed)
        except Exception:
            return None
    return None

def get_system_data():
    global prev_disk, prev_time

    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_freq_obj = psutil.cpu_freq()
    cpu_freq_mhz = cpu_freq_obj.current if cpu_freq_obj else None
    cpu_freq_ghz = round(cpu_freq_mhz / 1000, 2) if cpu_freq_mhz else None
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)
    cpu_name = platform.processor()

    # RAM
    ram = psutil.virtual_memory()
    ram_percent = ram.percent
    ram_used = round(ram.used / (1024**3), 2)
    ram_total = round(ram.total / (1024**3), 2)
    ram_speed = get_ram_speed()

    # CPU temperatur (Linux)
    cpu_temp = None
    if platform.system() == "Linux":
        temps = psutil.sensors_temperatures()
        if temps:
            for name, entries in temps.items():
                for entry in entries:
                    cpu_temp = entry.current
                    break

    # Disk
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_used = round(disk.used / (1024**3), 2)
    disk_total = round(disk.total / (1024**3), 2)

    # Disk read/write per sekund
    current_disk = psutil.disk_io_counters()
    current_time = time.time()
    elapsed = current_time - prev_time
    read_speed = round((current_disk.read_bytes - prev_disk.read_bytes) / (1024**2) / elapsed, 2)
    write_speed = round((current_disk.write_bytes - prev_disk.write_bytes) / (1024**2) / elapsed, 2)
    prev_disk = current_disk
    prev_time = current_time

    return {
        "cpu_percent": cpu_percent,
        "cpu_freq": cpu_freq_ghz,
        "cpu_cores": cpu_cores,
        "cpu_threads": cpu_threads,
        "cpu_name": cpu_name,
        "cpu_temp": cpu_temp,
        "ram_percent": ram_percent,
        "ram_used": ram_used,
        "ram_total": ram_total,
        "ram_speed": ram_speed,
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
    app.run(host="0.0.0.0", debug=True, port=5001)