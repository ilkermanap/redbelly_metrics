import time
from prometheus_client import start_http_server, Gauge
import subprocess

# Create a metric to track time spent and requests made.
block_height = Gauge('node_block_height', 'The latest block of this node')

LOGFILE="/var/log/redbelly/rbn_logs/rbbc_logs.log"

def find_last_block():
    cmd = subprocess.run(["tail", "-n", "20", LOGFILE], capture_output=True)
    blid = None
    for line in cmd.stdout.decode().splitlines():
        if line.find("Imported new chain segment")> -1:
            blid = line.split("{")[1].split(",")[0].split(":")[1].replace('"','')
            return(blid)
                     
        if line.find("with current local block") > -1:
            blid = line.split("with current local block")[1].split()[0]

    if blid is not None:
        return(blid)

def find_last_block_number():
    """A dummy function that takes some time."""
    blid = find_last_block()
    if blid is not None:
        block_height.set(int(blid))

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9101)
    # Generate some requests.
    while True:
        find_last_block_number()
        time.sleep(30)
