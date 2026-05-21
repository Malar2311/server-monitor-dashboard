from flask import Flask, render_template, Response
import psutil
from datetime import datetime
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import pytz
import os

app = Flask(__name__)

cpu_usage = Gauge('cpu_usage', 'CPU Usage')
memory_usage = Gauge('memory_usage', 'Memory Usage')
disk_usage = Gauge('disk_usage', 'Disk Usage')


@app.route("/")
def index():

    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    cpu_usage.set(cpu)
    memory_usage.set(memory)
    disk_usage.set(disk)

    # Indian time
    ist = pytz.timezone('Asia/Kolkata')
    last_updated = datetime.now(ist).strftime("%d %b %Y — %I:%M %p")

    return render_template(
        "index.html",
        cpu=cpu,
        memory=memory,
        disk=disk,
        last_updated=last_updated
    )


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
