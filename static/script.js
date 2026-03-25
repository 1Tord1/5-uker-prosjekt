function getColor(percent) {
    percent = Number(percent);
    if (percent < 50) return '#22c55e';
    if (percent < 80) return '#eab308';
    return '#ef4444';
}

function updateData() {
    fetch("/api/data")
        .then(res => res.json())
        .then(data => {
            // CPU
            const cpuPercent = Number(data.cpu_percent);
            const cpuBar = document.getElementById("cpu-bar");
            cpuBar.style.width = cpuPercent + "%";
            cpuBar.style.background = getColor(cpuPercent);
            document.getElementById("cpu-percent").textContent = cpuPercent + "%";
            cpuBar.querySelector(".inside").textContent = cpuPercent + "%";
            document.getElementById("cpu-freq").textContent = data.cpu_freq;
            document.getElementById("cpu-temp").textContent = data.cpu_temp;

            // RAM
            const ramPercent = Number(data.ram_percent);
            const ramBar = document.getElementById("ram-bar");
            ramBar.style.width = ramPercent + "%";
            ramBar.style.background = getColor(ramPercent);
            document.getElementById("ram-percent").textContent = ramPercent + "%";
            ramBar.querySelector(".inside").textContent = data.ram_used + " GB / " + data.ram_total + " GB";
            document.getElementById("ram-speed").textContent = data.ram_speed ? data.ram_speed : "N/A";

            // Disk
            const diskPercent = Number(data.disk_percent);
            const diskBar = document.getElementById("disk-bar");
            diskBar.style.width = diskPercent + "%";
            diskBar.style.background = getColor(diskPercent);
            document.getElementById("disk-percent").textContent = diskPercent + "%";
            diskBar.querySelector(".inside").textContent = data.disk_used + " GB / " + data.disk_total + " GB";
            document.getElementById("read-speed").textContent = data.read_speed;
            document.getElementById("write-speed").textContent = data.write_speed;
        })
        .catch(err => console.error(err));
}

setInterval(updateData, 1000);